import HomeAminate from "../animate/homeAnimate"

export default function Home({ setScreen, user }: { setScreen: any, user: any }) {
  const start = () => {
    setScreen('confirm')
  }
  return (
    <>
      <div className="w-full min-h-full grow flex flex-col bg-red-100">
        <div className="w-full max-w-vw mx-auto grow flex flex-col">
          <div className="p-5 flex items-center justify-between w-full max-w-[700px] mx-auto">
            <img src="/images/logo.svg" alt="" className="block w-20"></img>
            <img src="/images/avatar.svg" alt="" className="block w-8"></img>
          </div>
          <div className="mt-6 px-5 text-[32px] md:text-[56px] font-black leading-[1.2] md:text-center">
            <span className="text-red-50">Welcome back, </span><br className="lg:hidden" />
            <span className="text-white truncate">{user?.name}</span>
          </div>
          <div className="grow flex justify-center items-center" onClick={start}>
            <div className="my-auto flex justify-center relative">
              <HomeAminate></HomeAminate>
              <div className="absolute bottom-0 left-0 w-full translate-y-[50%] px-4 text-center text-white text-[20px] md:text-[28px] font-bold leading-[1.2]">Tap to add patient record</div>
            </div>
          </div>
          <div className="w-full pt-6 pb-2 flex items-center justify-center rounded-t-[20px] bg-white relative mt-auto">
            <div className="w-[28px] h-[3px] rounded-full bg-gray-50 absolute left-[50%] top-[12px] translate-x-[-50%] translate-y-[-50%]"></div>
            <div className="flex justify-center items-center gap-1">
              <img src="/images/icon-tips.svg" className="w-6 md:w-8" alt="" />
              <div className="text-[14px] md:text-[16px] mt-1"><strong className="text-red-100 tb-text-[18px]">Tips:</strong> Add website to home screen for easy access</div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}