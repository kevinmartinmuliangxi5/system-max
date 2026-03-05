import fs from 'node:fs';
import path from 'node:path';

const migrationPath = path.join(process.cwd(), 'src', 'db', 'migrations', '0001_initial_schema.sql');

export async function runInitialMigration(db: { execAsync: (sql: string) => Promise<unknown> }) {
  const sql = fs.readFileSync(migrationPath, 'utf8');
  await db.execAsync(sql);
}
