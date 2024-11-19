import FormLogin from "../form/formLogin";
import Logo from "../logo";

export default function Login({ setScreen, setUser }: { setScreen: any, setUser: any }) {
  return (
    <>
      <div className={`w-full min-h-full grow flex flex-col items-center overflow-hidden`}>
        <div className="w-full max-w-vw mx-auto grow overflow-auto flex flex-col">
          <div className="px-5 pb-5 z-10 relative flex flex-col grow">
            <div className="flex items-center justify-between shrink-0 relative z-10">
              <Logo></Logo>
            </div>
            <FormLogin setScreen={setScreen} setUser={setUser}></FormLogin>
          </div>
        </div>
      </div>
    </>
  )
}
