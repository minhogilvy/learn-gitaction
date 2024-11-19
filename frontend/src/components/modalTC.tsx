export default function ModalTC({ setModalTC }: { setModalTC: any }) {
  return (
    <div className="fixed top-0 left-0 w-full h-full z-modal bg-black/[.6] flex justify-center items-center p-5">
      <div className="w-full max-w-[320px] md:max-w-[565px] rounded-[20px] drop-shadow-modal bg-gray-25 overflow-hidden ">
        <div className="font-bold py-3 pl-5 pr-3 bg-red-25 flex items-center justify-between">
          Terms & Conditions
          <div className="size-10 shrink-0 rounded-full bg-white flex justify-center items-center" onClick={() => setModalTC(false)}>
            <img className="block size-6 shrink-0 object-contain" src="/images/icon-close.svg" alt="" />
          </div>
        </div>
        <div className="overflow-hidden max-h-[80vh] py-7 pl-5 pr-3 flex flex-col">
          <div className="text-[12px] leading-[1.4] font-light overflow-auto flex-1 pr-2 flex flex-col gap-4">
            <p>I  agree that by responding to, or having the information provided on my behalf to, the Screening Questions and submitting these Oral Screening Photos (collectively, “Data”) to Colgate, I am providing my irrevocable and express authorization and consent to Colgate to use, process, store, modify, combine with other data sets, disclose to authorized third party partners, or otherwise process such Data with or without your name, or any other attribution worldwide, in perpetuity, without compensation or other consideration, and hereby waive the right to inspect or approve Colgate’s use of these photos. Colgate’s use of Data may include, without limitation: account profile maintenance; improvement of products and services; research and development; training and improvement of our generative artificial intelligence models and other tools; security and fraud detection; analytics purposes; and other purposes consistent with our <span className="underline text-red-100">Privacy Policy</span>. I understand that Colgate is not obligated to use this Data. I hereby assign ownership of the Data to Colgate and understand that it will not be returned to me. I  hereby release, discharge and agree to hold Colgate and all persons acting under Colgate’s permission and authority, harmless from any and all claims, actions, demands, damages, losses, costs, charges, recoveries, judgments, penalties, liabilities and expenses (“Liabilities”), resulting from the use of this Data.</p>
            <p>Where applicable, I acknowledge, understand and voluntarily consent to my child(ren)’s participation in this oral screening and for my child(ren)’s personal data, including sensitive personal data, to be processed by Colgate as outlined above and in accordance with applicable data privacy and data protection laws. </p>
            <p>I confirm that I am of legal age and acknowledge and agree to Colgate’s <span className="underline text-red-100">Privacy Policy</span>. </p>
          </div>
        </div>
      </div>
    </div>
  )
}