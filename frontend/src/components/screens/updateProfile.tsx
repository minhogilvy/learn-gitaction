import FormUpdateProfile from "../form/formUpdateProfile";

export default function UpdateProfile({ setScreen, setUser }: { setScreen: any, setUser: any }) {
  return (
    <>
      <div className={`w-full min-h-full grow flex flex-col items-center overflow-hidden`}>
        <div className="w-full max-w-vw mx-auto grow overflow-auto flex flex-col">
          <div className="px-5 pb-5 z-10 relative flex flex-col grow">
            <div className="flex items-center justify-between shrink-0 relative z-10">
              <img src="/images/logo-variant-2.svg" className="block w-16"></img>
            </div>
            <FormUpdateProfile setScreen={setScreen} setUser={setUser}></FormUpdateProfile>
          </div>
        </div>
      </div>
    </>
  )
}