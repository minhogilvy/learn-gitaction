export default function Modal({
  children,
}: React.HTMLAttributes<HTMLElement>) {
  return (
    <div className="fixed top-0 left-0 w-full h-full z-modal bg-black/[.6] flex justify-center items-center p-5">
      <div className="w-full max-w-[320px] md:max-w-[464px] rounded-[20px] drop-shadow-modal bg-gray-25 overflow-hidden">
        {children}
      </div>
    </div>
  )
}