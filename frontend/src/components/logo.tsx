import { useState } from "react";
import Button from "./button";
import Modal from "./modal";
import { createPortal } from 'react-dom';

export default function Logo({ backToHome }: { backToHome?: any }) {
  const [showExitConfirm, setShowExitConfirm] = useState(false)
  return (
    <>
      <img src="/images/logo-variant-2.svg" className="block w-16 md:w-[100px]" onClick={() => setShowExitConfirm(!!backToHome)} alt=""></img>
      {showExitConfirm && createPortal(<Modal>
        <div className="p-5 flex flex-col items-center gap-2">
          <img src="/images/icon-error.svg" className="block w-[54px] shrink-0" alt="" />
          <div className="text-[20px] font-bold text-red-100 gap-2 text-center">Are you sure you<br />want to exit?</div>
          <div className="leading-[1.4] text-center">If you exit, this unfinished patient record will be deleted. Are you sure you want to continue?</div>
          <Button variant="white" onClick={() => setShowExitConfirm(false)}>Stay</Button>
          <div onClick={() => backToHome && backToHome()} className="text-[14px] text-gray-100 underline text-center mt-2 cursor-pointer">Exit Anyway</div>
        </div>
      </Modal>, document.body)}
    </>
  )
}