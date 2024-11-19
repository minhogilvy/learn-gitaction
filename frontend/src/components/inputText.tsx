export default function InputText({
  label,
  onChange,
  error,
  className,
  type,
  placeholder,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement> & { label?: string, error?: string, className?: string, type?: string, placeholder?: string }) {
  return (
    <div className={`relative pt-3 ${className}`}>
      {
        label && <label className="absolute block px-1.5 left-5 top-1 text-[14px] font-medium text-grey bg-white z-10">
          {label}
          <span className="w-1 h-1 bg-red-100 block absolute top-0 right-0 rounded-full"></span>
        </label>
      }
      <input placeholder={placeholder} className={`appearance-none w-full h-12 px-5 flex items-center rounded-full border focus:outline-none ${error ? "border-red-100 text-red-100" : "border-default text-default"}`} type={type || "text"} {...props} onChange={onChange} />
      {error && <div className="text-red-100 text-[14px] font-light leading-[1.4] tracking-[0.14px] mt-[10px]">{error}</div>}
    </div>
  );
}