export default function InputSelect({
  label,
  options,
  error,
  onChange,
  className,
  ...props
}: React.SelectHTMLAttributes<HTMLSelectElement> & { label?: string, options?: string[], error?: string, className?: string }) {
  return (
    <div className={"relative pt-3 " + className}>
      {
        label && <label className="absolute block px-1.5 left-5 top-1 text-[14px] font-medium text-grey bg-white z-10">
          {label}
          <span className="w-1 h-1 bg-red-100 block absolute top-0 right-0 rounded-full"></span>
        </label>
      }
      <select className={`w-full h-12 pl-5 pr-12 flex items-center rounded-full border focus:outline-none appearance-none bg-dropdown bg-white bg-no-repeat ${error ? "border-red-100 text-red-100" : "border-default text-default"}`} {...props} onChange={onChange}>
        {options?.map((option, index) => <option key={index} value={option}>{option}</option>)}
      </select>
      {error && <div className="text-red-100 text-[14px] font-light leading-[1.4] tracking-[0.14px] mt-[10px]">{error}</div>}
    </div>
  );
}