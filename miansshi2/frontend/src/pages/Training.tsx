// Training.tsx - 训练页面
import { useState } from 'react'
import { JobSelector } from '../components/JobSelector'
import { Recorder } from '../components/Recorder'
import { FeedbackPanel } from '../components/FeedbackPanel'
import { useJobCategory, useCurrentQuestion, useIsGeneratingQuestion, useSetGeneratingQuestion, useSetCurrentQuestion, useSetAnswerText } from '../store'
import { generateQuestion } from '../api'
import type { QuestionType } from '../types'

const QUESTION_TYPES: QuestionType[] = [
  '综合分析',
  '计划组织',
  '应急应变',
  '人际关系',
  '情景模拟',
]

// 详细题型答题技巧
const QUESTION_TIPS: Record<QuestionType, {
  steps: { name: string, desc: string, time: string }[],
  guidance: string,
  example: string,
  mistakes: string[],
  structure: string
}> = {
  '综合分析': {
    steps: [
      { name: '点', desc: '开门见山，表明观点态度', time: '30秒' },
      { name: '析', desc: '多角度分析原因、背景、影响', time: '1-2分钟' },
      { name: '对', desc: '提出具体可行的对策措施', time: '1-2分钟' },
      { name: '升', desc: '总结升华，体现政治高度', time: '30秒' }
    ],
    guidance: '透过现象看本质，结合时政热点，体现政治站位和大局意识。答题要有深度，避免泛泛而谈。注意正反两面分析，既要看到问题也要看到成绩。',
    example: '【题目】躺平现象\n【开头】"躺平现象反映了当代青年面临的现实困境，但我认为选择躺平并非长久之计。"\n【分析】社会压力大 + 竞争激烈 + 焦虑情绪\n【对策】完善社会保障 + 优化就业环境 + 引导正确价值观\n【升华】"青年是国家的未来，既要仰望星空，也要脚踏实地。"',
    mistakes: [
      '❌ 只谈问题不谈对策，纯吐槽',
      '❌ 观点模棱两可，没有明确立场',
      '❌ 脱离材料，空发议论',
      '❌ 没有时政高度，就事论事'
    ],
    structure: '表明态度(10%) + 分析原因(30%) + 提出对策(40%) + 总结升华(20%)'
  },
  '计划组织': {
    steps: [
      { name: '定', desc: '明确活动目的和目标', time: '30秒' },
      { name: '摸', desc: '调查摸底，了解实际情况', time: '30秒' },
      { name: '筹', desc: '人财物时地的筹备安排', time: '1分钟' },
      { name: '控', desc: '活动流程控制和应急预案', time: '30秒' },
      { name: '结', desc: '总结汇报和长效机制', time: '30秒' }
    ],
    guidance: '必须有【调查摸底】环节，方案要具体可落地。注意人、财、物、时、地的合理配置。活动要有预案，体现风险管理意识。',
    example: '【题目】组织一次消防安全检查\n【目的】消除隐患，确保安全\n【摸底】辖区有多少单位？重点在哪里？\n【筹备】成立检查组(3-5人) + 制定检查清单 + 时间安排\n【实施】分组检查 → 发现问题 → 当场整改/限期整改\n【总结】形成报告 + 跟踪整改 + 定期复查',
    mistakes: [
      '❌ 没有调查摸底，上来就干',
      '❌ 只有框架没有细节，空话套话',
      '❌ 忽略应急预案，缺少风险意识',
      '❌ 结尾没有长效机制'
    ],
    structure: '目的(10%) + 摸底(20%) + 筹备(30%) + 实施(30%) + 总结(10%)'
  },
  '应急应变': {
    steps: [
      { name: '稳', desc: '控制局面，安抚情绪', time: '30秒' },
      { name: '明', desc: '了解情况，判断性质', time: '30秒' },
      { name: '调', desc: '调动资源，协调各方', time: '30秒' },
      { name: '解', desc: '解决问题，消除隐患', time: '1分钟' },
      { name: '报', desc: '向上级汇报', time: '15秒' },
      { name: '总', desc: '反思总结，完善机制', time: '15秒' }
    ],
    guidance: '首要任务是【控制局面】，处理顺序要得当。分清轻重缓急，先急后缓，先人后事。注意区分公事私事，不越权也不推诿。',
    example: '【题目】群众在办事大厅情绪激动，与工作人员争吵\n【稳】"您先消消气，有什么问题我来帮您解决"\n【明】了解事情经过，是工作人员态度问题还是政策问题？\n【解】\n  → 态度问题：道歉，批评教育\n  → 政策问题：耐心解释，提供替代方案\n【报】向领导汇报处理情况\n【总】加强培训，优化流程',
    mistakes: [
      '❌ 一上来就解释，没有先安抚情绪',
      '❌ 顺序错误，先处理小事忽略大事',
      '❌ 只顾眼前解决，没有后续跟进',
      '❌ 越权处理或推卸责任'
    ],
    structure: '控制局面(20%) + 了解情况(20%) + 解决问题(40%) + 汇报总结(20%)'
  },
  '人际关系': {
    steps: [
      { name: '态度', desc: '尊重理解，反思自己', time: '30秒' },
      { name: '原因', desc: '换位思考，找出根源', time: '30秒' },
      { name: '化解', desc: '沟通交流，积极补救', time: '1分钟' },
      { name: '避免', desc: '建立长效机制', time: '30秒' }
    ],
    guidance: '核心原则：工作为重。严禁"老好人"思想，原则问题不退让。要体现高情商和职业素养。注意区分对上级、对同事、对群众的不同处理方式。',
    example: '【题目】同事工作中不配合，导致项目延误\n【态度】"可能是我沟通不够，让他对工作安排有误解"\n【原因】信息不对称？利益冲突？个人情绪？\n【化解】\n  → 主动沟通，了解对方的困难和顾虑\n  → 寻求共识，强调团队目标\n  → 适当妥协，但不违背原则\n【避免】建立定期沟通机制，明确分工职责',
    mistakes: [
      '❌ 一味迁就，变成"老好人"',
      '❌ 只站在自己立场，不换位思考',
      '❌ 公事私事混为一谈',
      '❌ 没有原则底线'
    ],
    structure: '态度表态(20%) + 分析原因(30%) + 沟通化解(40%) + 总结避免(10%)'
  },
  '情景模拟': {
    steps: [
      { name: '入戏', desc: '完全代入角色身份', time: '10秒' },
      { name: '共情', desc: '理解对方感受，拉近距离', time: '30秒' },
      { name: '说理', desc: '用对方能接受的方式讲道理', time: '1分钟' },
      { name: '表态', desc: '给出具体承诺或解决方案', time: '30秒' }
    ],
    guidance: '必须真正【入戏】，语气和表情要符合身份。用第一人称作答，直接与对象对话。注意称呼和语气要符合身份关系。',
    example: '【题目】你是社区工作人员，劝说居民配合拆迁工作\n【入戏】我是社区工作者老王，面对的是住了几十年的老邻居\n【开场】"张大爷，我是小王啊，您坐，咱们聊聊"\n【共情】"我理解您的顾虑，这房子住了大半辈子，感情深啊"\n【说理】"但您看，这次改造对咱们小区是好事啊，环境能改善，房价也能涨..."\n【表态】"您放心，我会全程帮您办好手续，有困难随时找我"\n【收尾】"您先考虑考虑，明天我再来听您意见"',
    mistakes: [
      '❌ 没有入戏，用第三人称描述',
      '❌ 语气生硬，不像在对话',
      '❌ 只讲大道理，没有共情',
      '❌ 身份定位错误，越权表态'
    ],
    structure: '开场(10%) + 共情(20%) + 劝说(50%) + 表态(20%)'
  },
}

export function Training() {
  const jobCategory = useJobCategory()
  const currentQuestion = useCurrentQuestion()
  const isGeneratingQuestion = useIsGeneratingQuestion()
  const setGeneratingQuestion = useSetGeneratingQuestion()
  const setCurrentQuestion = useSetCurrentQuestion()
  const setAnswerText = useSetAnswerText()

  const [selectedType, setSelectedType] = useState<QuestionType>('综合分析')
  const [showJobSelector, setShowJobSelector] = useState(false)
  const [showTips, setShowTips] = useState(false)

  const handleGenerateQuestion = async () => {
    if (!jobCategory) {
      setShowJobSelector(true)
      return
    }

    setGeneratingQuestion(true)
    setAnswerText('')

    try {
      const question = await generateQuestion(jobCategory, selectedType)
      setCurrentQuestion(question)
    } catch (error) {
      console.error('生成题目失败:', error)
      alert('生成题目失败，请稍后重试')
    } finally {
      setGeneratingQuestion(false)
    }
  }

  // 获取当前题型技巧
  const currentTips = currentQuestion ? QUESTION_TIPS[currentQuestion.question_type] : null

  return (
    <div className="min-h-screen">
      {/* 页面头部 */}
      <div className="flex items-center justify-between px-10 py-8">
        <div className="space-y-1">
          <h1 className="text-3xl font-semibold text-gray-900">训练模式</h1>
          <p className="text-sm text-gray-500">AI生成题目，即时反馈，针对性提升</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            练习记录
          </button>
          <button
            onClick={handleGenerateQuestion}
            disabled={isGeneratingQuestion}
            className="flex items-center gap-2 px-4 py-2.5 bg-red-600 rounded-lg text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            {isGeneratingQuestion ? '生成中...' : '生成新题目'}
          </button>
        </div>
      </div>

      {/* 题型选择 */}
      <div className="px-10 pb-4">
        <div className="flex gap-2">
          {QUESTION_TYPES.map((type) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`px-4 py-2 text-sm rounded-full border transition-all ${
                selectedType === type
                  ? 'bg-red-600 text-white border-red-600'
                  : 'bg-white text-gray-600 border-gray-200 hover:border-red-300'
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      {/* 主内容区 */}
      <div className="flex gap-6 px-10 pb-10" style={{ height: 'calc(100vh - 200px)' }}>
        {/* 左栏：题目 + 作答 */}
        <div className="flex-1 flex flex-col gap-5">
          {/* 题目卡片 */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            {currentQuestion ? (
              <>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <span className="px-3 py-1 bg-red-50 text-red-600 text-xs font-medium rounded-md">
                      {currentQuestion.question_type}
                    </span>
                  </div>
                  <button
                    onClick={() => setShowTips(true)}
                    className="flex items-center gap-2 px-3 py-1.5 border border-gray-200 rounded-md hover:bg-yellow-50 hover:border-yellow-300 transition-colors cursor-pointer"
                  >
                    <svg className="w-4 h-4 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    <span className="text-xs text-yellow-700 font-medium">答题技巧</span>
                  </button>
                </div>
                <p className="text-base text-gray-800 leading-relaxed">{currentQuestion.question_text}</p>
                <div className="flex gap-4 mt-4 text-xs text-gray-500">
                  <span>建议作答时间：3-5分钟</span>
                  <span>建议字数：200-500字</span>
                </div>
              </>
            ) : (
              <div className="text-center py-8 text-gray-400">
                <p>点击"生成新题目"开始练习</p>
                {!jobCategory && (
                  <p className="text-sm text-red-500 mt-2">请先在侧边栏选择岗位类型</p>
                )}
              </div>
            )}
          </div>

          {/* 作答卡片 */}
          <div className="flex-1 bg-white rounded-xl border border-gray-200 p-6 flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-semibold text-gray-900">语音回答</h3>
              {currentQuestion && (
                <span className="px-2.5 py-1 bg-green-50 text-green-600 text-xs rounded-md">
                  准备就绪
                </span>
              )}
            </div>

            <div className="flex-1 flex flex-col items-center justify-center">
              <Recorder />
            </div>
          </div>
        </div>

        {/* 右栏：AI反馈 */}
        <div className="w-[360px]">
          <FeedbackPanel />
        </div>
      </div>

      {/* 岗位选择弹窗 */}
      {showJobSelector && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-[400px] max-h-[80vh] overflow-auto">
            <h3 className="text-lg font-semibold mb-4">请先选择岗位类型</h3>
            <JobSelector />
            <button
              onClick={() => setShowJobSelector(false)}
              className="mt-4 w-full py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
            >
              关闭
            </button>
          </div>
        </div>
      )}

      {/* 答题技巧弹窗 - 增强版 */}
      {showTips && currentTips && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl w-[700px] max-h-[90vh] overflow-hidden flex flex-col">
            {/* 标题栏 */}
            <div className="flex items-center justify-between p-5 border-b border-gray-200 bg-gradient-to-r from-red-50 to-orange-50">
              <div>
                <h3 className="text-lg font-bold text-gray-900">
                  {currentQuestion?.question_type} - 答题技巧
                </h3>
                <p className="text-xs text-gray-500 mt-1">建议作答时间：3-5分钟 | 建议字数：200-500字</p>
              </div>
              <button
                onClick={() => setShowTips(false)}
                className="text-gray-400 hover:text-gray-600 p-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* 内容区 */}
            <div className="flex-1 overflow-auto p-5 space-y-5">
              {/* 答题步骤 - 带时间分配 */}
              <div>
                <h4 className="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <span className="w-6 h-6 bg-red-600 text-white rounded-full flex items-center justify-center text-xs">1</span>
                  答题步骤与时间分配
                </h4>
                <div className="grid grid-cols-2 gap-2">
                  {currentTips.steps.map((step, index) => (
                    <div
                      key={index}
                      className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="w-8 h-8 bg-red-600 text-white text-sm font-bold rounded-lg flex items-center justify-center flex-shrink-0">
                        {step.name}
                      </div>
                      <div className="flex-1">
                        <div className="text-sm font-medium text-gray-800">{step.desc}</div>
                        <div className="text-xs text-gray-500 mt-0.5">{step.time}</div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-2 p-2 bg-blue-50 rounded text-xs text-blue-700">
                  💡 答题结构：{currentTips.structure}
                </div>
              </div>

              {/* 评分要点 */}
              <div>
                <h4 className="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <span className="w-6 h-6 bg-yellow-500 text-white rounded-full flex items-center justify-center text-xs">2</span>
                  评分要点
                </h4>
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-sm text-gray-700 leading-relaxed">{currentTips.guidance}</p>
                </div>
              </div>

              {/* 示例回答 */}
              <div>
                <h4 className="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <span className="w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-xs">3</span>
                  示例回答框架
                </h4>
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans leading-relaxed">{currentTips.example}</pre>
                </div>
              </div>

              {/* 常见错误 */}
              <div>
                <h4 className="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <span className="w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs">4</span>
                  常见错误（避免！）
                </h4>
                <div className="space-y-2">
                  {currentTips.mistakes.map((mistake, index) => (
                    <div key={index} className="flex items-center gap-2 p-2 bg-red-50 rounded-lg">
                      <span className="text-red-500 text-sm">{mistake}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* 当前题目提示 */}
              {currentQuestion && (
                <div className="bg-gray-100 rounded-lg p-4">
                  <h4 className="text-sm font-semibold text-gray-800 mb-2">📋 当前题目</h4>
                  <p className="text-sm text-gray-700">{currentQuestion.question_text}</p>
                </div>
              )}
            </div>

            {/* 底部按钮 */}
            <div className="p-4 border-t border-gray-200 bg-gray-50">
              <button
                onClick={() => setShowTips(false)}
                className="w-full py-2.5 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium"
              >
                开始作答
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
