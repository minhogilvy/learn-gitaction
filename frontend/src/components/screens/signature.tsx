import { useEffect, useRef, useState } from "react";
import Button from "../button";
import Modal from "../modal";
import Logo from "../logo";
import ModalTC from "../modalTC";


export default function Signature({ setScreen, setSignature, backToHome }: { setScreen: any, setSignature: any, backToHome: any }) {
  const canvasEl = useRef<null | HTMLCanvasElement>(null)
  const ctx = useRef<null | CanvasRenderingContext2D>(null)
  const [agreed, setAgreed] = useState(false)
  const drawing = useRef(false)
  const [showError, setShowError] = useState(false)
  const [showTC, setShowTC] = useState(false)

  const getTouchPoint = (e: TouchEvent) => {
    const bounding = canvasEl.current?.getBoundingClientRect()
    return {
      x: e.touches[0].clientX - (bounding?.left || 0),
      y: e.touches[0].clientY - (bounding?.top || 0)
    }
  }
  const onTouchStart = (e: TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    const touch = e.touches[0]
    if (!ctx.current || !touch) return
    drawing.current = true


    ctx.current.beginPath()
    ctx.current.strokeStyle = "black"
    ctx.current.lineWidth = 2
    ctx.current.lineJoin = "round";
    ctx.current.lineCap = "round";
    const { x, y } = getTouchPoint(e)
    ctx.current.moveTo(x, y)
  }

  const onTouchMove = (e: TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    const touch = e.touches[0]
    if (!ctx.current || !touch || !drawing.current) return

    const { x, y } = getTouchPoint(e)
    ctx.current.lineTo(x, y)
    ctx.current.stroke()
  }

  const onTouchEnd = (e: TouchEvent) => {
    e.preventDefault()
    if (!drawing) return
    drawing.current = false
  }
  const init = (el: HTMLCanvasElement) => {
    el.width = el.offsetWidth
    el.height = el.offsetHeight
    ctx.current = el.getContext("2d")
    el.addEventListener("touchstart", onTouchStart)
    el.addEventListener("touchmove", onTouchMove)
    el.addEventListener("touchend", onTouchEnd)
  }

  const reset = () => {
    if (!canvasEl.current) return
    const ctx = canvasEl.current.getContext("2d")
    ctx?.clearRect(0, 0, canvasEl.current.width, canvasEl.current.height)
  }

  useEffect(() => {
    if (!canvasEl.current) return
    init(canvasEl.current)
  }, [])

  const submit = async () => {
    setShowError(false)
    if (!agreed) {
      alert("Please agree to consent")
      return
    }
    const ctx = canvasEl.current?.getContext("2d")
    const imageData = ctx?.getImageData(0, 0, canvasEl.current!.width, canvasEl.current!.height)
    if (!imageData?.data?.filter(item => item > 0).length || imageData?.data?.filter(item => item > 0).length! < 100) return
    const signature = canvasEl.current?.toDataURL("image/png")
    setSignature(signature)
    setScreen('addPatient')
  }

  return (
    <>
      <div className={`fixed top-0 left-0 w-full min-h-full grow flex flex-col items-center overflow-hidden`}>
        <div className="w-full grow flex flex-col overflow-auto">
          <div className="grow w-full max-w-[768px] lg:max-w-[864px] mx-auto relative pb-10">
            <div className="absolute top-0 left-0 w-full h-[180px] rounded-b-[24px] bg-red-25 sm:hidden pointer-events-none"></div>
            <div className="absolute top-0 left-0 w-full h-[180px] rounded-b-[24px] bg-red-25 sm:h-[265px] hidden sm:block lg:hidden pointer-events-none" style={{ clipPath: "ellipse(1480px 2000px at 50% -1736px)" }}></div>
            <div className="px-5 z-10 relative">
              <div className="flex items-center justify-between shrink-0 relative z-10">
                <Logo backToHome={backToHome}></Logo>
              </div>
              <div className="w-full lg:flex lg:gap-20 lg:mt-10">
                <div className="lg:mt-16">
                  <div className="mt-2 text-[28px] font-bold text-center">Patient Signature</div>
                  <div className="mt-2 text-[14px] text-center">Please sign below to confirm your consent.</div>
                </div>
                <div className="mt-5 sm:mt-10 lg:mt-0">
                  <div className="w-full max-w-[378px] mx-auto aspect-square rounded-[16px] border border-gray-100 bg-white overflow-hidden relative">
                    <canvas ref={canvasEl} className="w-full h-full"></canvas>
                    <div className="flex items-center gap-2 absolute bottom-2 right-2 text-gray-75" onClick={reset}>
                      Reset
                      <img src="/images/icon-reset.svg" className="size-5 shrink-0" alt="" />
                    </div>
                  </div>
                  <div className="mt-4 flex items-center sm:justify-center gap-3">
                    <div className={`w-9 aspect-square shrink-0 rounded-[8px] border border-gray-100 flex items-center justify-center ${agreed ? "bg-default" : "bg-white"}`} onClick={() => setAgreed(!agreed)}>
                      {agreed && (<img className="block w-4" src="/images/icon-check.svg" alt="" />)}
                    </div>
                    <div className="text-[14px] font-light">I have read & agree to the <span className="underline font-normal" onClick={() => setShowTC(true)}>Privacy Policy</span> and <span className="underline font-normal" onClick={() => setShowTC(true)}>Terms & Conditions</span></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="w-full h-[60px] sm:h-[100px] shrink-0 flex justify-center items-center mt-auto shadow-[0_-3px_28.6px_0_rgba(0,0,0,0.15)]">
          <Button className="mx-auto" onClick={submit}>
            <div className="flex gap-3 items-center">
              Submit
            </div>
          </Button>
        </div>
      </div>
      {showError && (<Modal>
        <div className="p-5 flex flex-col items-center gap-2">
          <img src="/images/icon-error.svg" className="block w-[54px] shrink-0" alt="" />
          <div className="text-[20px] font-bold text-red-100 gap-2">Submission Failed</div>
          <div className="leading-[1.4] text-center">There was a problem submitting the data. Please check your internet connection and try again.</div>
          <Button variant="white" onClick={submit}>Retry</Button>
        </div>
      </Modal>)}
      {showTC && (<ModalTC setModalTC={setShowTC}></ModalTC>)}
    </>
  )
}