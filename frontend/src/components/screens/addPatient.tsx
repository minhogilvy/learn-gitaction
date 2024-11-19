import Button from "@/components/button";
import InputSelect from "@/components/inputSelect";
import InputText from "@/components/inputText";
import { addPatient } from "@/lib/helper";
import { useState } from "react";
import Modal from "../modal";
import Logo from "../logo";

export default function AddPatient({ setScreen, setPatientId, backToHome }: { setScreen: any, setPatientId: any, backToHome: any }) {
  const [loading, setLoading] = useState(false)
  const [showError, setShowError] = useState(false)
  const [formData, setFormData] = useState<{ [key: string]: { value: string, error: string } }>({
    fullName: {
      value: "",
      error: ""
    },
    age: {
      value: "",
      error: ""
    },
    email: {
      value: "",
      error: ""
    },
    country: {
      value: "South Africa",
      error: ""
    },
    race_ethnicity: {
      value: "African",
      error: ""
    },
    // fullName: {
    //   value: "abc",
    //   error: ""
    // },
    // age: {
    //   value: "30",
    //   error: ""
    // },
    // email: {
    //   value: "abc@gmail.com",
    //   error: ""
    // },
    // country: {
    //   value: "South Africa",
    //   error: ""
    // },
    // race_ethnicity: {
    //   value: "African",
    //   error: ""
    // },
  })

  const setData = (key: string, value: string) => {
    setFormData((prev) => ({ ...prev, [key]: { value, error: "" } }))
  }
  const setError = (key: string, error: string) => {
    setFormData((prev) => ({ ...prev, [key]: { value: prev[key].value, error } }))
  }

  const validate = () => {
    let isValid = true
    if (!formData.fullName.value.trim()) {
      setError("fullName", "Full name is required")
      isValid = false
    }
    if (!formData.age.value.trim()) {
      setError("age", "Age is required")
      isValid = false
    } else if (Number(formData.age.value) < 1 || Number(formData.age.value) > 99) {
      setError("age", "Age should be between 1 and 99​")
      isValid = false
    }
    if (!formData.email.value.trim()) {
      setError("email", "Email is required")
      isValid = false
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(formData.email.value)) {
      setError("email", "Invalid email address")
      isValid = false
    }
    if (!formData.country.value.trim()) {
      setError("country", "Country is required")
      isValid = false
    }
    if (!formData.race_ethnicity.value.trim()) {
      setError("race_ethnicity", "Race/Ethnicity is required")
      isValid = false
    }

    return isValid
  }

  const onSubmit = (e: any) => {
    e.preventDefault()
    submit()
  }
  const submit = async () => {
    setShowError(false)
    if (validate()) {
      setLoading(true)
      const res = await addPatient({
        fullName: formData.fullName.value,
        age: Number(formData.age.value),
        email: formData.email.value,
        country: formData.country.value,
        raceEthnicity: formData.race_ethnicity.value
      })
      setLoading(false)
      if (res?.success) {
        setPatientId(res?.data?.userId)
        setScreen('capture')
      } else {
        setShowError(true)
      }
    }
  }
  return (
    <>
      <div className={`w-full max-w-vw mx-auto flex-1 flex flex-col overflow-auto  ${loading && "pointer-events-none"}`}>
        <div className="px-5 flex items-center justify-between shrink-0">
          <Logo backToHome={backToHome}></Logo>
        </div>
        <div className="my-auto pb-4 max-w-[568px] mx-auto">
          <div className="px-5 mt-4 pb-5 md:text-center">
            <div className="text-[28px] font-bold">New Patient Record</div>
            <div className="mt-2 text-gray-100 text-[14px] font-light max-w-[400px] mx-auto">{`This information will be anonymized and used to train Colgate's AI models to improve dental care.`}</div>
          </div>
          <form onSubmit={onSubmit} className="px-5 flex flex-col gap-3 md:gap-6">
            <InputText label="Full name" value={formData.fullName.value} error={formData.fullName.error} required onChange={(e) => setData("fullName", e.target.value)}></InputText>
            <InputText type="number" min={1} max={99} label="Age" value={formData.age.value} error={formData.age.error} required onChange={(e) => setData("age", e.target.value)}></InputText>
            <InputText label="Email" value={formData.email.value} error={formData.email.error} required onChange={(e) => setData("email", e.target.value)}></InputText>
            <InputSelect key="selectCountry" label="Country" value={formData.country.value} error={formData.country.error} options={["South Africa", "Tanzania", "Nigeria", "Kenya"]} required onChange={(e) => setData("country", e.target.value)}></InputSelect>
            <InputSelect key="selectEthnicity" label="Race/Ethnicity" value={formData.race_ethnicity.value} error={formData.country.error} options={["African", "United States", "Canada", "Mexico"]} required onChange={(e) => setData("race_ethnicity", e.target.value)}></InputSelect>
            <button className="hidden"></button>
          </form>
        </div>
      </div>
      <div className={`w-full h-[60px] md:h-[100px] shrink-0 flex justify-center items-center mt-auto shadow-[0_-3px_28.6px_0_rgba(0,0,0,0.15)] ${loading && "pointer-events-none"}`}>
        <Button className="mx-auto" onClick={submit} loading={loading}>
          Next
        </Button>
      </div>
      {showError && (<Modal>
        <div className="p-5 flex flex-col items-center gap-2">
          <img src="/images/icon-error.svg" className="block w-[54px] shrink-0" alt="" />
          <div className="text-[20px] font-bold text-red-100 gap-2">Submission Failed</div>
          <div className="leading-[1.4] text-center">There was a problem submitting the data. Please check your internet connection and try again.</div>
          <Button variant="white" onClick={submit}>Retry</Button>
        </div>
      </Modal>)}
      
    </>
  )
} 