export default function Test() {
  return (
    <div className="w-full h-screen flex items-center justify-center bg-dark">
      <div className="w-[640px] aspect-square relative overflow-hidden">
        <img className="w-full" src="/images/64443413-832.webp" alt="" />
        <div className="scan-grid absolute w-full h-full top-0 left-0"></div>
        <div className="scan-decorate absolute w-full h-full top-0 left-0"></div>
        <div className="scan-line"></div>
      </div>
    </div>
  )
}