import { useRouter } from "next/router";
import Button from "../button";

export default function ResetSuccess() {
  const router = useRouter()
  return (
    <>
      <div className={`w-full min-h-full grow flex flex-col items-center overflow-hidden`}>
        <div className="w-full max-w-vw mx-auto grow overflow-auto flex flex-col">
          <div className="px-5 pb-5 z-10 relative flex flex-col grow">
            <div className="flex items-center justify-between shrink-0 relative z-10">
              <img src="/images/logo-variant-2.svg" className="block w-16"></img>
            </div>
            <div className="w-full my-auto flex flex-col">
              <svg className="w-[57px] mx-auto" width="57" height="57" viewBox="0 0 57 57" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="56.1908" height="56.1908" rx="28.0954" fill="#D2010D" />
                <path d="M22.372 33.4751L41.2298 14.6174L45.2646 18.6808L33.8183 30.1271L22.372 41.5733L10.9258 30.1271L14.9606 26.0923L22.372 33.4751Z" fill="white" />
              </svg>
              <div className="bg-[url('/images/form-deco.png')] bg-top bg-no-repeat mt-7 flex flex-col">
                <div className="text-[28px] font-black text-center">You can now log in with your new password</div>
                <Button type="button" className="mx-auto mt-12" onClick={() => router.push("/")}>Back to Login</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
