export default function InputRate({
  label,
  onChange,
  value,
  className,
}: React.InputHTMLAttributes<HTMLInputElement> & { label?: string, onChange?: (value?: number) => void, className?: string, value?: number | null }) {
  return (
    <div className={"py-3 " + className}>
      <div className="lg:text-[14px]">{label}</div>
      <div className="w-full h-4 flex items-center rounded-full bg-gray-25 mt-2">
        <div className="w-1/4 h-full flex items-center justify-center relative" onClick={() => onChange?.(0)}>
          <div className={`aspect-square rounded-full absolute left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] ${value === 0 ? "w-6 border-[3px] border-red-100 bg-white" : "w-2 bg-gray-50"}`}></div>
        </div>
        <div className="w-1/4 h-full flex items-center justify-center relative" onClick={() => onChange?.(1)}>
          <div className={`aspect-square rounded-full absolute left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] ${value === 1 ? "w-6 border-[3px] border-red-100 bg-white" : "w-2 bg-gray-50"}`}></div>
        </div>
        <div className="w-1/4 h-full flex items-center justify-center relative" onClick={() => onChange?.(2)}>
          <div className={`aspect-square rounded-full absolute left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] ${value === 2 ? "w-6 border-[3px] border-red-100 bg-white" : "w-2 bg-gray-50"}`}></div>
        </div>
        <div className="w-1/4 h-full flex items-center justify-center relative" onClick={() => onChange?.(3)}>
          <div className={`aspect-square rounded-full absolute left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] ${value === 3 ? "w-6 border-[3px] border-red-100 bg-white" : "w-2 bg-gray-50"}`}></div>
        </div>
      </div>
      <div className="w-full h-4 flex items-center text-gray-100 text-center text-[11px] mt-2">
        <div className={`w-1/4 h-full flex items-center justify-center relative ${value === 0 && "text-red-100 font-bold"}`} onClick={() => onChange?.(0)}>
          Undetected
        </div>
        <div className={`w-1/4 h-full flex items-center justify-center relative ${value === 1 && "text-red-100 font-bold"}`} onClick={() => onChange?.(1)}>
          Fair
        </div>
        <div className={`w-1/4 h-full flex items-center justify-center relative ${value === 2 && "text-red-100 font-bold"}`} onClick={() => onChange?.(2)}>
          Medium
        </div>
        <div className={`w-1/4 h-full flex items-center justify-center relative ${value === 3 && "text-red-100 font-bold"}`} onClick={() => onChange?.(3)}>
          Poor
        </div>
      </div>
    </div>
  );
}