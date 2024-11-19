import ScreenResetPassword from "@/components/screens/resetPassword";
import ResetSuccess from "@/components/screens/resetSuccess";
import { useState } from "react";

export default function ResetPassword() {
  const [screen, setScreen] = useState<"resetPassword" | "resetSuccess">("resetPassword")
  return (
    <>
      {screen === "resetPassword" && <ScreenResetPassword setScreen={setScreen}></ScreenResetPassword>}
      {screen === "resetSuccess" && <ResetSuccess></ResetSuccess>}
    </>
  )
}