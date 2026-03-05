import initSqlJs, {
  type BindParams,
  type Database,
  type QueryExecResult,
} from 'sql.js';

type AsyncDb = {
  execAsync: (sql: string) => Promise<void>;
  runAsync: (sql: string, ...params: unknown[]) => Promise<void>;
};

export type SqlJsTestDb = {
  raw: Database;
  asyncDb: AsyncDb;
  scalar: (sql: string) => number;
  text: (sql: string) => string;
};

export async function createSqlJsTestDb(): Promise<SqlJsTestDb> {
  const SQL = await initSqlJs({
    locateFile: (file) => require.resolve(`sql.js/dist/${file}`),
  });
  const raw = new SQL.Database();

  return {
    raw,
    asyncDb: {
      execAsync: async (sql: string) => {
        raw.exec(sql);
      },
      runAsync: async (sql: string, ...params: unknown[]) => {
        raw.run(sql, params as BindParams);
      },
    },
    scalar: (sql: string) => {
      const rows = raw.exec(sql);
      return readNumber(rows);
    },
    text: (sql: string) => {
      const rows = raw.exec(sql);
      return readString(rows);
    },
  };
}

function readNumber(rows: QueryExecResult[]): number {
  const value = rows[0]?.values?.[0]?.[0];
  if (typeof value === 'number') {
    return value;
  }
  if (typeof value === 'bigint') {
    return Number(value);
  }
  return Number(value ?? 0);
}

function readString(rows: QueryExecResult[]): string {
  const value = rows[0]?.values?.[0]?.[0];
  return String(value ?? '');
}
