import { useEffect, useRef, useState } from "react"
import Modal from "../modal";
import Button from "../button";
import { claim, predictTeeth } from "@/lib/helper";
import EditImage from "./editImage";
import { ImageError, Pov } from "@/pages";

export type ImageEditorType = { imageData: string, imageToScan: string, scale: number, rotate: number, translate: { x: number, y: number }, imageError: ImageError }

export default function Capture(
  { setScreen, pov, setTeethImage, patientId, back }:
    { setScreen: any, pov: Pov, setTeethImage: any, patientId: string, back: any }) {
  const videoEl = useRef<HTMLVideoElement>(null)
  const [videoConfig, setVideoConfig] = useState<{ width: number, height: number }>({ width: 0, height: 0 })
  const [tabletLanscape, setTabletLandscape] = useState(0)
  const [imageData, setImageData] = useState<null | string>(null);
  const offCanvasEl = useRef<null | HTMLCanvasElement>(null)
  const [showTutorial, setShowTutorial] = useState(true);
  const [localStep, setLocalStep] = useState<"capture" | "scan" | "scanSuccess" | "edit">("capture")
  const stream = useRef<MediaStream | null>(null)
  const [showAPIError, setShowAPIError] = useState(false)
  const [imageError, setImageError] = useState<ImageError>("")
  const [editingImage, setEditingImage] = useState<ImageEditorType>({
    imageData: "",
    imageToScan: "",
    scale: 1,
    rotate: 0,
    translate: { x: 0, y: 0 },
    imageError: ""
  })

  const capture = async () => {
    if (!offCanvasEl.current || !videoEl.current) return;
    offCanvasEl.current?.getContext("2d")?.drawImage(videoEl.current, 0, 0, offCanvasEl.current.offsetWidth, offCanvasEl.current.offsetHeight);
    const base64 = offCanvasEl.current.toDataURL()
    setImageData(base64)
    setEditingImage(prev => ({ ...prev, imageData: base64, imageToScan: base64 }))
    setLocalStep("scan")
    await predict({ image: base64 })
  };

  const predict = async ({ image }: { image: string }) => {
    setImageError("")
    setShowAPIError(false)
    setLocalStep("scan")
    if (!image || !pov || !patientId) return;
    const res = await predictTeeth({
      // image: sample[pov],
      image,
      pov,
      userId: patientId
    })
    if (!res?.success) {
      setShowAPIError(true)
    } else if (res?.data.code) {
      setImageError(res?.data.code)
      setLocalStep("edit")
    } else {
      setLocalStep("scanSuccess")
      setTeethImage(image)
      setTimeout(() => {
        setScreen("rate")
      }, 2000);
    }
  };

  const requestCamera = async (constraints: MediaStreamConstraints = {
    video: {
      facingMode: "environment",
    }
  }) => {
    // let stream: MediaStream | null;
    try {
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      return stream || null
      /* use the stream */
    } catch (err) {
      /* handle the error */
      console.error(err)
      return null
    }
  }

  const start = async () => {
    const minSize = Math.min(document.body.clientWidth, window.innerHeight)
    const videoSize = claim(minSize, 512, 768)
    stream.current = await requestCamera({
      video: {
        width: videoSize,
        height: videoSize,
        aspectRatio: 1,
        facingMode: "environment",
      },
    });
    if (!stream.current) {
      setScreen("home")
      return
    };
    const config = stream.current?.getVideoTracks()[0].getSettings();
    setVideoConfig({
      width: config?.width || 512,
      height: config?.height || 512,
    });
    setLocalStep("capture");
    requestAnimationFrame(() => {
      if (videoEl.current) {
        videoEl.current.srcObject = stream.current;
        videoEl.current?.play();
      }
    });
  };



  useEffect(() => {
    const resizeObserver = new ResizeObserver(() => {
      const bounding = videoEl.current?.getBoundingClientRect()
      setTabletLandscape(document.body.clientWidth - (bounding?.right || 0))
    });
    if (videoEl.current) {
      resizeObserver?.observe(videoEl.current as Element);
    }
    start();
  }, []);

  useEffect(() => {
    window.requestAnimationFrame(() => {
      if (localStep === "capture") {
        if (videoEl.current) {
          start()
        }
      } else {
        stream.current?.getTracks()[0].stop()
      }
    })
  }, [localStep]);

  return (
    <>
      <div className={`w-full min-h-full grow flex flex-col items-center bg-dark overflow-auto`}>
        <div className="w-full max-w-vw lg:max-w-full mx-auto relative">
          <div className="px-5 h-16 flex items-center justify-between md:absolute md:top-0 md:left-[50%] md:translate-x-[-50%] w-full z-[20]">
            {localStep === "capture" && (
              <>
                <div className="flex items-center gap-2 text-white" onClick={back}>
                  <img src="/images/btn-back.svg" className="block w-[40px]"></img>
                  Back
                </div>
                <img src="/images/btn-question.svg" className="block w-[40px]" onClick={() => setShowTutorial(true)}></img>
              </>
            )}
            {localStep === "edit" && (
              <>
                <div className="flex items-center gap-2 text-white" onClick={() => setLocalStep("capture")}>
                  <img src="/images/retake.svg" className="block w-[40px]"></img>
                  Retake photo
                </div>
                <img src="/images/btn-question.svg" className="block w-[40px]"></img>
              </>
            )}
          </div>
          <div className="w-full max-w-[768px] mx-auto aspect-square relative z-1">
            {localStep === "capture" && (
              <div className="top-0 left-0 w-full aspect-square relative">
                <video
                  className="aspect-square w-full"
                  style={{ width: videoConfig.width }}
                  ref={videoEl}
                  playsInline
                ></video>
                <div className="absolute top-0 left-0 w-full h-full z-10">
                  <img className="w-full" src="/images/camera/grid.svg" alt=""></img>
                  {pov === "frontTeeth" && (
                    <div className="absolute top-0 left-0 w-full h-full bg-[url(/images/camera/frame-front.svg)] bg-cover z-10 text-center text-white leading-[1.4] px-4 pt-3">
                      <div className="md:w-[450px] mx-auto md:mt-5 md:text-[24px]">
                        {`Position the patient's front teeth within the frame and tap the capture button`}
                      </div>
                    </div>
                  )}
                  {pov === "upperJaw" && (
                    <div className="absolute top-0 left-0 w-full h-full bg-[url(/images/camera/frame-upper.svg)] bg-cover z-10 text-center text-white leading-[1.4] px-4 pt-3">
                      {`Position the patient's upper teeth within the frame and tap the capture button`}</div>
                  )}
                  {pov === "lowerJaw" && (
                    <div className="absolute top-0 left-0 w-full h-full bg-[url(/images/camera/frame-lower.svg)] bg-cover z-10 text-center text-white leading-[1.4] px-4 pt-3">
                      {`Position the patient's lower teeth within the frame and tap the capture button`}</div>
                  )}
                </div>
              </div>
            )}
            {(localStep === "scan" || localStep === "scanSuccess") && !!imageData && (
              <div className="top-0 left-0 w-full aspect-square relative overflow-hidden">
                <img src={editingImage.imageToScan} alt="" className="block w-full h-full object-cover" />
                {localStep === "scan" && (
                  <>
                    <div className="scan-grid absolute w-full h-full top-0 left-0"></div>
                    <div className="scan-line"></div>
                  </>
                )}
              </div>
            )}
            {localStep === "edit" && (
              <div className="md:w-[560px] mx-auto md:mt-20">
                <EditImage pov={pov} imageError={imageError} editingImage={editingImage} setEditingImage={setEditingImage} predict={predict} setImageData={setImageData}></EditImage>
              </div>
            )}
            <canvas
              ref={offCanvasEl}
              width={videoConfig.width}
              height={videoConfig.height}
              className="opacity-0 absolute top-0 left-[-9999px] pointer-events-none"
            ></canvas>
          </div>
        </div>
        {localStep === "capture" && (
          <div className="py-5 my-auto flex justify-center items-center z-[21] landscape:lg:absolute landscape:lg:right-0 landscape:lg:top-0 landscape:lg:flex-col landscape:lg:h-full landscape:lg:w-auto" style={{ right: `${(tabletLanscape - 76) / 2}px` }}>
            <div className="w-[76px] aspect-square bg-[url(/images/btn-capture.svg)] bg-contain cursor-pointer" onClick={capture}></div>
          </div>
        )}
        {localStep === "scan" && (
          <div className="my-10 px-5 flex justify-center items-center text-[14px] md:text-[20px] text-white text-center">Scanning photo in progess...</div>
        )}
        {localStep === "scanSuccess" && (
          <div className="my-10 px-5 flex justify-center items-center text-[14px] md:text-[20px] text-white text-center h-10">
            <img src="/images/scan-success.gif" className="size-[95px] -mr-4 shrink-0" />
            Scanning success
          </div>
        )}
      </div>
      {showTutorial && (<Modal>
        {pov === "frontTeeth" && (
          <>
            <div className="h-12 md:h-16 bg-red-25 flex justify-center items-center text-[18px] font-bold text-center">Take the picture of Front teeth</div>
            <div className="py-5 md:py-10 px-[14px] md:px-12 flex flex-wrap -mx-[6px] md:-mx-5">
              <div className="w-1/2 px-[6px] md:px-5">
                <img src="/images/tut-1.png" className="w-full aspect-square bg-contain"></img>
                <div className="text-[14px] leading-[1.4] mt-[10px] text-center">Make sure both the patient’s teeth and gums are clearly visible in the frame.</div>
              </div>
              <div className="w-1/2 px-[6px] md:px-5">
                <img src="/images/tut-2.png" className="w-full aspect-square bg-contain"></img>
                <div className="text-[14px] leading-[1.4] mt-[10px] text-center">The photo should look like this</div>
              </div>
            </div>
          </>
        )}
        {pov === "upperJaw" && (
          <>
            <div className="h-12 bg-red-25 flex justify-center items-center text-[18px] font-bold text-center">Take the picture of Upper teeth</div>
            <div className="py-5 px-[14px] flex flex-wrap -mx-[6px]">
              <div className="w-1/2 px-[6px]">
                <img src="/images/tut-3.png" className="w-full aspect-square bg-contain"></img>
                <div className="text-[14px] leading-[1.4] mt-[10px] text-center">Ask the patient to open their mouth wide and focus the photo on the upper teeth.</div>
              </div>
              <div className="w-1/2 px-[6px]">
                <img src="/images/tut-4.png" className="w-full aspect-square bg-contain"></img>
                <div className="text-[14px] leading-[1.4] mt-[10px] text-center">The photo should look like this</div>
              </div>
            </div>
          </>
        )}
        {pov === "lowerJaw" && (
          <>
            <div className="h-12 bg-red-25 flex justify-center items-center text-[18px] font-bold text-center">Take the picture of Lower teeth</div>
            <div className="py-5 px-[14px] flex flex-wrap -mx-[6px]">
              <div className="w-1/2 px-[6px]">
                <img src="/images/tut-5.png" className="w-full aspect-square bg-contain"></img>
                <div className="text-[14px] leading-[1.4] mt-[10px] text-center">Ask the patient to open their mouth wide and focus the photo on the lower teeth.</div>
              </div>
              <div className="w-1/2 px-[6px]">
                <img src="/images/tut-6.png" className="w-full aspect-square bg-contain"></img>
                <div className="text-[14px] leading-[1.4] mt-[10px] text-center">The photo should look like this</div>
              </div>
            </div>
          </>
        )}
        <div className="flex justify-center pb-3">
          <Button variant="secondary" className="!w-[226px]" onClick={() => setShowTutorial(false)}>Got It</Button>
        </div>
      </Modal>)}
      {showAPIError && (<Modal>
        <div className="p-5 flex flex-col items-center gap-2">
          <img src="/images/icon-error.svg" className="block w-[54px] shrink-0" alt="" />
          <div className="text-[20px] font-bold text-red-100 gap-2">Submission Failed</div>
          <div className="leading-[1.4] text-center">There was a problem submitting the data. Please check your internet connection and try again.</div>
          <Button variant="white" onClick={() => predict({ image: imageData! })}>Retry</Button>
        </div>
      </Modal>)}
    </>
  )
}