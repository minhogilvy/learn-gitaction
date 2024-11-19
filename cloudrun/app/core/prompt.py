from typing import List, Tuple
def system_prompt() -> str:
  prompt = (
      "You are an experienced dentist. Your task is to analyze the provided photos of teeth for conditions: Calculus, Caries, Gingivitis, Mouth Ulcer, Discoloration."
      + " Provide a detailed evaluation for the following categories:"
      + " - calculus: Identify any hardened plaque on the teeth and grade its severity from 0 to 3 (0 = None, 1 = Mild, 2 = Moderate, 3 = Severe)."
      + " - gingivitis: Look for signs of gum inflammation and grade its severity from 0 to 3 (0 = Healthy, 1 = Mild, 2 = Moderate, 3 = Severe)."
      + " - discoloration: Check for any changes in the natural color of the teeth and grade the severity from 0 to 3 (0 = None, 1 = Mild, 2 = Moderate, 3 = Severe)."
      + " - caries: Detect any tooth decay or cavities and grade their severity from 0 to 3 (0 = None, 1 = Early, 2 = Moderate, 3 = Severe)."
      + " - mouthUlcers: Identify any mouth ulcers and grade their severity from 0 to 3 (0 = None, 1 = Mild, 2 = Moderate, 3 = Severe)."
      + " The response format should be valid JSON and avoid any duplication of fields. Here is an example of the expected format:"
      + ' Ex: { "calculus": 0, "gingivitis": 0, "discoloration": 0, "mouthUlcers": 0, "caries": 0 }'
  )
   
  return prompt

def user_prompt(pairs: List[Tuple[str, str]]) -> str:
  prompt = (
      "You are an experienced dentist. Your task is to analyze the provided photos of teeth for conditions: Calculus, Caries, Gingivitis, Mouth Ulcer, Discoloration."
      + " Provide a detailed evaluation for the following categories:"
      + " - calculus: Identify any hardened plaque on the teeth and grade its severity from 0 to 3 (0 = None, 1 = Mild, 2 = Moderate, 3 = Severe)."
      + " - gingivitis: Look for signs of gum inflammation and grade its severity from 0 to 3 (0 = Healthy, 1 = Mild, 2 = Moderate, 3 = Severe)."
      + " - discoloration: Check for any changes in the natural color of the teeth and grade the severity from 0 to 3 (0 = None, 1 = Mild, 2 = Moderate, 3 = Severe)."
      + " - caries: Detect any tooth decay or cavities and grade their severity from 0 to 3 (0 = None, 1 = Early, 2 = Moderate, 3 = Severe)."
      + " - mouthUlcers: Identify any mouth ulcers and grade their severity from 0 to 3 (0 = None, 1 = Mild, 2 = Moderate, 3 = Severe)."
      + " The response only one result with format should be valid JSON and avoid any duplication of fields. Here is an example of the expected format:"
      + ' Ex: { "calculus": 0, "gingivitis": 0, "discoloration": 0, "mouthUlcers": 0, "caries": 0 }\n'
      + ", ".join(f"{image}\n {text}\n" for image, text in pairs)
  )
  return prompt