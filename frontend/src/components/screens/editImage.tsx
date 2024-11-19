import { useEffect, useRef, useState } from "react"
import RotateIndicator from "../imageEditor/rotateIndicator"
import { Pov } from "@/pages"
import Button from "../button"
import html2canvas from 'html2canvas';
import { ImageEditorType } from "./capture";
import RotateIndicatorVerticle from "../imageEditor/rotateIndicatorVerticle";

export default function EditImage({ pov, imageError, editingImage, setEditingImage, predict }: { pov: Pov, setImageData: any, imageError: string, editingImage: ImageEditorType, setEditingImage: any, predict: any }) {
  // const [rotate, setRotate] = useState(0)
  // const [scale, setScale] = useState(1)
  const scaleRef = useRef(1)
  const minScale = useRef(1)
  const rotateRef = useRef(0)
  const translateRef = useRef({ x: 0, y: 0 })
  // const [translate, setTranslate] = useState({ x: 0, y: 0 })
  const pointerOrigin = useRef<{ x: number, y: number }[]>([])
  const scaleOrigin = useRef(1)
  const translating = useRef(false)
  const zooming = useRef(false)
  const editorRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const forceUpdate = useState<number>(0)
  const setScale = (scale: number) => {
    setEditingImage(prev => ({ ...prev, scale }))
  }
  const setTranslate = (translate: { x: number, y: number }) => {
    setEditingImage(prev => ({ ...prev, translate }))
  }
  const setRotate = (rotate: number) => {
    setEditingImage(prev => ({ ...prev, rotate }))
  }

  const errors = {
    incorrect_angle: "Incorrect angle. Please position the camera directly in front of the patient's teeth.",
    unable_to_detect: "Unable to detect teeth in the image. Please ensure the patient's front teeth are clearly visible within the frame.",
    image_is_too_dark: "Image is too dark. Please improve the lighting or use the flash.",
    image_is_blurry: "Image is blurry. Please hold the camera steady and try again."
  }

  const updateRotate = (_rotate: number) => {
    rotateRef.current = _rotate
    setRotate(_rotate)
  }

  const onTouchStart = (e: TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (!e.touches.length) return
    if (e.touches.length === 1) {
      translating.current = true
      zooming.current = false
    } else {
      zooming.current = true
      translating.current = false
    }
    pointerOrigin.current = Array.from(e.touches).map(t => ({
      x: t.clientX,
      y: t.clientY
    }))
    scaleOrigin.current = scaleRef.current
  }
  const onTouchMove = (e: TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (translating.current) {
      const touch = e.touches[0]
      const origin = pointerOrigin.current[0]
      const margin = {
        x: touch.clientX - origin.x,
        y: touch.clientY - origin.y
      }

      const newPoint = {
        x: translateRef.current.x + margin.x,
        y: translateRef.current.y + margin.y
      }
      const offset = (Math.sqrt(Math.pow(newPoint.x, 2) + Math.pow(newPoint.y, 2)))
      const originWidth = editorRef.current?.offsetWidth || 0
      const rotatedOriginWidth = originWidth * Math.max(1, ((Math.abs(Math.sin(rotateRef.current))) + Math.abs(Math.cos((rotateRef.current)))))
      const scaledWidth = originWidth * scaleRef.current
      const maxRange = (scaledWidth - rotatedOriginWidth) / 2
      const canTranslate = offset < maxRange
      if (canTranslate) {
        translateRef.current = newPoint
        setTranslate(newPoint)
      }
    } else if (zooming.current && e.touches.length >= 2) {
      const dist = Math.sqrt(Math.pow(e.touches[0].clientX - e.touches[1].clientX, 2) + Math.pow(e.touches[0].clientY - e.touches[1].clientY, 2))
      const distPrev = Math.sqrt(Math.pow(pointerOrigin.current[0].x - pointerOrigin.current[1].x, 2) + Math.pow(pointerOrigin.current[0].y - pointerOrigin.current[1].y, 2))
      scaleRef.current = Math.max(minScale.current, scaleRef.current * (dist / distPrev))
    }
    pointerOrigin.current = Array.from(e.touches).map(t => ({
      x: t.clientX,
      y: t.clientY
    }))
    forceUpdate?.[1]?.(Date.now())
  }

  const onTouchEnd = (e: TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    translating.current = false
    scaleOrigin.current = scaleRef.current
  }

  const submit = () => {
    html2canvas(containerRef.current!).then(canvas => {
      const base64Image = canvas.toDataURL("image/png")
      setEditingImage(prev => ({ ...prev, imageToScan: base64Image }))
      predict({ image: base64Image })
    })
  }

  const getDistance = (p1: { x: number, y: number }, p2: { x: number, y: number }) => {
    return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2))
  }

  const getAngle = (p1: { x: number, y: number }, p2: { x: number, y: number }) => {
    return Math.atan2(p2.y - p1.y, p2.x - p1.x)
  }

  const getMinScaleOnRotate = () => {
    const tl = { x: -editorRef.current?.offsetWidth! / 2, y: -editorRef.current?.offsetHeight! / 2, angle: 0 }
    const tr = { x: editorRef.current?.offsetWidth! / 2, y: -editorRef.current?.offsetHeight! / 2, angle: 0 }
    const bl = { x: -editorRef.current?.offsetWidth! / 2, y: editorRef.current?.offsetHeight! / 2, angle: 0 }
    const br = { x: editorRef.current?.offsetWidth! / 2, y: editorRef.current?.offsetHeight! / 2, angle: 0 }
    const center = { ...editingImage.translate }
    tl.angle = getAngle({ x: tl.x, y: tl.y }, { ...center }) - editingImage.rotate
    tr.angle = getAngle({ x: tr.x, y: tr.y }, { ...center }) - editingImage.rotate
    bl.angle = getAngle({ x: bl.x, y: bl.y }, { ...center }) - editingImage.rotate
    br.angle = getAngle({ x: br.x, y: br.y }, { ...center }) - editingImage.rotate
    return Math.max(
      getDistance(tl, center) * Math.abs(Math.cos(tl.angle)) / (editorRef.current?.offsetWidth! / 2),
      getDistance(tr, center) * Math.abs(Math.cos(tr.angle)) / (editorRef.current?.offsetWidth! / 2),
      getDistance(bl, center) * Math.abs(Math.cos(bl.angle)) / (editorRef.current?.offsetWidth! / 2),
      getDistance(br, center) * Math.abs(Math.cos(br.angle)) / (editorRef.current?.offsetWidth! / 2),
      getDistance(tl, center) * Math.abs(Math.sin(tl.angle)) / (editorRef.current?.offsetWidth! / 2),
      getDistance(tr, center) * Math.abs(Math.sin(tr.angle)) / (editorRef.current?.offsetWidth! / 2),
      getDistance(bl, center) * Math.abs(Math.sin(bl.angle)) / (editorRef.current?.offsetWidth! / 2),
      getDistance(br, center) * Math.abs(Math.sin(br.angle)) / (editorRef.current?.offsetWidth! / 2),
    )
  }

  useEffect(() => {
    editorRef.current?.addEventListener("touchstart", onTouchStart)
    editorRef.current?.addEventListener("touchmove", onTouchMove)
    editorRef.current?.addEventListener("touchend", onTouchEnd)
    return () => {
      editorRef.current?.removeEventListener("touchstart", onTouchStart)
      editorRef.current?.removeEventListener("touchmove", onTouchMove)
      editorRef.current?.removeEventListener("touchend", onTouchEnd)
    }
  }, [])

  useEffect(() => {
    setScale(scaleRef.current)
  }, [scaleRef.current])

  useEffect(() => {
    minScale.current = getMinScaleOnRotate()
    scaleRef.current = Math.max(scaleRef.current, getMinScaleOnRotate())

    setScale(scaleRef.current)
  }, [editingImage.rotate])

  useEffect(() => {
    minScale.current = getMinScaleOnRotate()
  }, [editingImage.translate])

  return (
    <>
      <div className="px-[10px] pointer-events-none">
        <div className="w-full relative">
          <div ref={editorRef} className="w-full aspect-square relative bg-white/50 overflow-hidden pointer-events-auto">
            <div ref={containerRef} className="absolute top-0 left-0 w-full h-full translate" style={{ transform: `translate(${editingImage.translate.x}px, ${editingImage.translate.y}px)` }}>
              <div className="absolute top-0 left-0 w-full h-full rotate" style={{ transform: `rotate(${editingImage.rotate}rad)` }}>
                <div className="absolute top-0 left-0 w-full h-full zoom" style={{ transform: `scale(${editingImage.scale})` }}>
                  <img src={editingImage.imageData} alt="" />
                </div>
              </div>
            </div>
            <div className="absolute top-0 left-0 w-full h-full z-10 pointer-events-none">
              {pov === "frontTeeth" && <img className="absolute top-0 left-0 w-full h-full" src="/images/camera/frame-front.svg" alt=""></img>}
              {pov === "upperJaw" && <img className="absolute top-0 left-0 w-full h-full" src="/images/camera/frame-upper.svg" alt=""></img>}
              {pov === "lowerJaw" && <img className="absolute top-0 left-0 w-full h-full" src="/images/camera/frame-lower.svg" alt=""></img>}
              <img className="absolute top-0 left-0 w-full h-full" src="/images/camera/grid.svg" alt=""></img>
              <img className="absolute top-0 left-0 w-full h-full" src="/images/camera/crop-frame.svg" alt=""></img>
            </div>
          </div>
          <div className="absolute top-0 left-full h-full py-5 ml-5 flex-col hidden landscape:lg:flex pointer-events-auto">
            <RotateIndicatorVerticle onChange={updateRotate} defaultRotate={editingImage.rotate}></RotateIndicatorVerticle>
          </div>
        </div>
      </div>
      <div className="px-5 mt-5 landscape:lg:hidden">
        <RotateIndicator onChange={updateRotate} defaultRotate={editingImage.rotate}></RotateIndicator>
      </div>
      <div className="px-4">
        {!!errors[imageError] && (
          <div className="flex gap-2 text-red-100 p-3 rounded-[12px] my-4" style={{ background: "linear-gradient(92deg, #F8D9DB 0.56%, rgba(248, 217, 219, 0.90) 99.74%)" }}>
            {imageError === "incorrect_angle" && (
              <img className="w-6 shrink-0" src="/images/camera/icon-error-rotate.svg" alt="" />
            )}
            {imageError === "unable_to_detect" && (
              <img className="w-6 shrink-0" src="/images/camera/icon-error-detect.svg" alt="" />
            )}
            {imageError === "image_is_too_dark" && (
              <img className="w-6 shrink-0" src="/images/camera/icon-error-brightness.svg" alt="" />
            )}
            {imageError === "image_is_blurry" && (
              <img className="w-6 shrink-0" src="/images/camera/icon-error-blurry.svg" alt="" />
            )}
            {errors[imageError]}
          </div>
        )}
      </div>
      <div className="mt-auto mb-2 px-5 flex justify-center">
        <Button className="mt-6 mb-2" onClick={submit}>Next</Button>
      </div>
    </>
  )
}
