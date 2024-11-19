import { useEffect, useRef, useState } from "react"

export default function RotateIndicatorVerticle({ defaultRotate, onChange }: { defaultRotate: number, onChange: (rotate: number) => void }) {
  const rotateIndicatorEl = useRef<HTMLDivElement | null>(null)
  const indicatorFocus = useRef(false)
  const pointerOrigin = useRef({ x: 0, y: 0 })
  const rotate = useRef(defaultRotate)
  const [rotateDeg, setRotateDeg] = useState(0)
  const [rotateIndicatorOffset, setRotateIndicatorOffset] = useState(0)

  const onTouchStart = (e: TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    indicatorFocus.current = true
    const touch = e.touches[0]
    if (!touch) return
    pointerOrigin.current = {
      x: touch.clientX,
      y: touch.clientY
    }
  }
  const onTouchMove = (e: TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (!indicatorFocus.current) return
    const touch = e.touches[0]
    if (!touch) return

    rotate.current = Math.min(Math.PI, Math.max(-Math.PI, rotate.current + ((touch.clientY - pointerOrigin.current.y) * 2) / 360))
    const radToDeg = rotate.current * 180 / Math.PI
    setRotateIndicatorOffset(radToDeg * rotateIndicatorEl.current!.offsetHeight / 180)
    setRotateDeg(~~((radToDeg) % 360))
    onChange(rotate.current)
    pointerOrigin.current = {
      x: touch.clientX,
      y: touch.clientY
    }
  }

  const onTouchEnd = (e: TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    indicatorFocus.current = false
  }
  useEffect(() => {
    const radToDeg = rotate.current * 180 / Math.PI
    setRotateIndicatorOffset(radToDeg * rotateIndicatorEl.current!.offsetWidth / 180)
    setRotateDeg(~~((radToDeg) % 360))
    rotateIndicatorEl.current?.addEventListener("touchstart", onTouchStart)
    rotateIndicatorEl.current?.addEventListener("touchmove", onTouchMove)
    rotateIndicatorEl.current?.addEventListener("touchend", onTouchEnd)
    return () => {
      rotateIndicatorEl.current?.removeEventListener("touchstart", onTouchStart)
      rotateIndicatorEl.current?.removeEventListener("touchmove", onTouchMove)
      rotateIndicatorEl.current?.removeEventListener("touchend", onTouchEnd)
    }
  }, [])
  return (
    <>
      <div className="flex grow">
        <div ref={rotateIndicatorEl} className="w-6 h-full relative bg-rotate-indicator-verticle" style={{ backgroundPositionY: `${rotateIndicatorOffset}px` }}>
          <div className="absolute h-[3px] w-[28px] top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] bg-red-100"></div>
        </div>
        <div className="text-center text-gray-50 my-auto ml-2 md:text-[26px]">{rotateDeg}°</div>
      </div>
    </>
  )
}