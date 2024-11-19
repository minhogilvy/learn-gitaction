import { useMemo, useState } from "react";
import Button from "../button";
import InputRate from "../inputRate";
import { Pov } from "@/pages";
import Logo from "../logo";

export default function Rate({ imageData, updateRate, pov, loading, backToHome }: { imageData: string | null, updateRate: any, pov: Pov, loading: boolean, backToHome: any }) {
  const [data, setData] = useState({
    "calculusGrade": null,
    "cariesGrade": null,
    "discolorationGrade": null,
    "gingivitisGrade": null,
    "mouthUlcerGrade": null
  })

  const isValid = useMemo(() => {
    return data.calculusGrade !== null && data.cariesGrade !== null && data.discolorationGrade !== null && data.gingivitisGrade !== null && data.mouthUlcerGrade !== null
  }, [data])
  const updateData = (key: string, value: number) => {
    setData((prev) => ({ ...prev, [key]: value }))
  }
  const submit = () => {
    if (!isValid) return
    updateRate(data)
  }
  return (
    <div className={`w-full min-h-full grow flex flex-col items-center overflow-hidden ${loading && "pointer-events-none"}`}>
      <div className="w-full grow flex flex-col overflow-auto ">
        <div className="grow relative w-full max-w-vw lg:max-w-[864px] mx-auto">
          <div className="absolute top-0 left-0 w-full h-[120px] rounded-b-[24px] bg-red-25 md:hidden pointer-events-none"></div>
          <div className="absolute top-0 left-0 w-full h-[120px] rounded-b-[24px] bg-red-25 md:h-[265px] hidden md:block lg:hidden pointer-events-none" style={{ clipPath: "ellipse(1480px 2000px at 50% -1736px)" }}></div>
          <div className="px-5 flex items-center justify-between shrink-0 relative z-10">
            <Logo backToHome={backToHome}></Logo>
          </div>
          <div className="w-full lg:flex lg:gap-20 lg:mt-10">
            <div className="px-5 mt-3 relative lg:px-0 lg:mt-0 lg:w-[360px] lg:shrink-0">
              <img src={imageData!} className="w-full aspect-square rounded-[16px] border-2 border-red-100 drop-shadow-moda max-w-[320px] lg:max-w-none mx-auto" alt="" />
            </div>
            <div className="flex-1">
              <div className="px-5 mt-4 sm:text-center lg:text-left lg:px-0 lg:mt-0">
                <div className="text-[28px] font-bold text-red-100">Rate the {pov === "frontTeeth" ? "Front" : pov === "upperJaw" ? "Upper" : "Lower"} Teeth condition</div>
                <div className="text-[14px] font-light tracking-[0.14px] text-gray-100 mt-2 sm:max-w-[450px] mx-auto">Please tap on the grading bar to select the option that best represents your opinion.</div>
              </div>
              <div className="px-5 mt-4 mb-10 lg:px-0">
                <div className="sm:max-w-[500px] mx-auto">
                  <InputRate label="Calculus" onChange={(value) => updateData("calculusGrade", value!)} value={data.calculusGrade as any}></InputRate>
                  <div className="w-full h-[1px] bg-gray-25"></div>
                  <InputRate className="lg:mt-2" label="Gingivitis" onChange={(value) => updateData("cariesGrade", value!)} value={data.cariesGrade as any}></InputRate>
                  <div className="w-full h-[1px] bg-gray-25"></div>
                  <InputRate className="lg:mt-2" label="Caries" onChange={(value) => updateData("discolorationGrade", value!)} value={data.discolorationGrade as any}></InputRate>
                  <div className="w-full h-[1px] bg-gray-25"></div>
                  <InputRate className="lg:mt-2" label="Discoloration" onChange={(value) => updateData("gingivitisGrade", value!)} value={data.gingivitisGrade as any}></InputRate>
                  <div className="w-full h-[1px] bg-gray-25"></div>
                  <InputRate className="lg:mt-2" label="Mouth ulcer" onChange={(value) => updateData("mouthUlcerGrade", value!)} value={data.mouthUlcerGrade as any}></InputRate>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="w-full h-[60px] md:h-[100px] shrink-0 flex justify-center items-center mt-auto shadow-[0_-3px_28.6px_0_rgba(0,0,0,0.15)]">
        <Button className={`mx-auto ${!isValid && 'pointer-events-none grayscale opacity-50'}`} onClick={submit} loading={loading}>Next</Button>
      </div>
    </div>
  )
}