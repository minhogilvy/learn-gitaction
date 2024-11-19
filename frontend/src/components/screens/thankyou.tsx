import ThankyouAminate from "../animate/thankyouAnimate";
import Button from "../button";

export default function Thankyou({ backToHome, newRecord }: { backToHome: any, newRecord: any }) {
  return (
    <>
      <div className="w-full min-h-full grow flex flex-col items-center overflow-auto">
        <div className="w-full max-w-vw lg:max-w-[864px] mx-auto grow flex flex-col">
          <div className="px-5 pb-5 z-10 relative flex flex-col grow">
            <div className="flex items-center justify-between shrink-0 relative z-10">
              <img src="/images/logo-variant-2.svg" className="block w-16 md:w-[100px]"></img>
              <img src="/images/avatar-red.svg" className="block w-8"></img>
            </div>
            <div className="flex items-center justify-center gap-10 my-auto">
              <ThankyouAminate className="w-[400px] hidden lg:block"></ThankyouAminate>
              <div className="flex flex-col justify-center">
                <div className="text-[28px] font-bold text-red-100 mt-9 lg:mt-0 text-center">Thank you!</div>
                <div className="leading-[1.4] text-center mt-10 lg:mt-5 lg:max-w-[300px]">Your contribution is valuable to the future of dentistry.</div>
                <div className="flex justify-center mt-9">
                <ThankyouAminate className="lg:hidden"></ThankyouAminate>
                </div>
                <Button className="mx-auto mt-10 md:mt-[100px] lg:mt-10" onClick={newRecord}>Add Patient Record</Button>
                <Button className="mx-auto mt-5" variant="secondary" onClick={backToHome}>Homepage</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}