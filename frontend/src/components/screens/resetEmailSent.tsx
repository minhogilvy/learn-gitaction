import Button from "../button";
import Logo from "../logo";

export default function ResetEmailSent({ setScreen, backToHome }: { setScreen: any, backToHome: any }) {
  return (
    <>
      <div className={`w-full min-h-full grow flex flex-col items-center overflow-hidden`}>
        <div className="w-full max-w-vw mx-auto grow overflow-auto flex flex-col">
          <div className="px-5 pb-5 z-10 relative flex flex-col grow">
            <div className="flex items-center justify-between shrink-0 relative z-10">
              <Logo backToHome={() => backToHome()}></Logo>
            </div>
            <div className="w-full my-auto flex flex-col">
              <svg className="w-[57px] mx-auto" width="57" height="57" viewBox="0 0 57 57" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="56.1908" height="56.1908" rx="28.0954" fill="#D2010D" />
                <path d="M22.372 33.4751L41.2298 14.6174L45.2646 18.6808L33.8183 30.1271L22.372 41.5733L10.9258 30.1271L14.9606 26.0923L22.372 33.4751Z" fill="white" />
              </svg>
              <div className="bg-[url('/images/form-deco.png')] bg-top bg-no-repeat mt-7 flex flex-col">
                <div className="text-[28px] font-black text-center">Please check<br />Your Email</div>
                <div className="text-center leading-[1.4] mt-7">
                  If you have an account with us, a password reset email has been sent.<br />
                  Please check your inbox (and spam folder). If you don&apos;t receive an email, please contact support.
                </div>
                <Button type="button" className="mx-auto mt-10" onClick={() => setScreen('login')}>Back to Login</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
