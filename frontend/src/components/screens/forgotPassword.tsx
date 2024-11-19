import FormForgotPassword from "../form/formForgotPassword";
import Logo from "../logo";

export default function ForgotPassword({ setScreen }: { setScreen: any }) {
  return (
    <>
      <div className={`w-full min-h-full grow flex flex-col items-center overflow-hidden`}>
        <div className="w-full max-w-vw mx-auto grow overflow-auto flex flex-col">
          <div className="px-5 pb-5 z-10 relative flex flex-col grow">
            <div className="flex items-center justify-between shrink-0 relative z-10">
              <Logo backToHome={() => setScreen('login')}></Logo>
            </div>
            <FormForgotPassword setScreen={setScreen}></FormForgotPassword>
          </div>
        </div>
      </div>
    </>
  )
}
