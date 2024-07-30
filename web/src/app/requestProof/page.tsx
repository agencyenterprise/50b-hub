"use client";

import { useState } from "react";
import { twMerge } from 'tailwind-merge';
import Button from "@/components/Button";
import { toast } from "react-toastify";
import JsonInputComponent from "@/components/JsonInputComponent";
import { isValidJson } from "../../../utils/json";

const modelOptions = [
  {
    name: "Iris model",
    modelId: "iris_model",
    description: "This model generates a prediction on whether you are a human being or a ladybird",
  },
  {
    name: "Incoming model",
    description: "Incoming model",
  },
]

export default function RequestProofPage() {
  const [jsonInput, setJsonInput] = useState<string>("");
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedModelOption, setSelectedModelOption] = useState<number | undefined>();
  const [description, setDescription] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    setLoading(true);

    if (
      selectedModelOption === undefined ||
      description.length === 0 ||
      name.length === 0 ||
      !isValidJson(jsonInput)
    ) return;

    console.log({
      name,
      description,
      ai_model_name: modelOptions[selectedModelOption].modelId,
      ai_model_inputs: jsonInput
    })

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_HUB_URL}/proof_requests`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: "include",
        body: JSON.stringify({
          name,
          description,
          ai_model_name: modelOptions[selectedModelOption].modelId,
          ai_model_inputs: jsonInput
        }),
      });

      if (response.ok) {
        toast.success("Logged with success");
        window.location.href = "/me";
      } else {
        response.json().then((data) => {
          toast.error(data.detail);
        })
      }
    } catch (error) {
      console.error("Failed to register user", error);
    }

  };

  return (
    <div className="relative bg-gray-900 h-screen">
      <form
        action="#"
        method="POST"
        className="px-6 pb-24 pt-20 sm:pb-32 lg:px-8 lg:py-40"
        onSubmit={handleSubmit}
      >
        <div className="mx-auto max-w-xl lg:max-w-lg">
          {
            currentStep === 1 && (
              <>
                <h3 className="text-2xl font-bold tracking-tight text-white pb-6">
                  Select the model
                </h3>
                <div className="grid grid-cols-2 gap-8">
                  {
                    modelOptions && modelOptions.map((model, index) => (
                      <button
                        key={index}
                        className={twMerge(
                          "flex flex-col max-w-sm p-4 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700",
                          selectedModelOption === index && "bg-gray-100 dark:bg-gray-700"
                        )}
                        onClick={() => setSelectedModelOption(index)}
                      >
                        <h4 className="text-left mb-2 text-lg font-bold tracking-tight text-gray-900 dark:text-white">
                          {model.name}
                        </h4>
                        <p className="text-left text-sm text-gray-700 dark:text-gray-400">
                          {model.description}
                        </p>
                      </button>
                    ))
                  }
                </div>
                <div className="flex items-end justify-end">
                  <Button
                    id="continue"
                    onClick={() => setCurrentStep(2)}
                    label="Continue"
                    className="mt-4"
                    disabled={
                      selectedModelOption !== 0
                    }
                  />
                </div>
              </>
            )
            || currentStep === 2 && (
              <>
                <h3 className="text-2xl font-bold tracking-tight text-white pb-6">
                  Proof request name and description
                </h3>
                <h2 className="tracking-tight text-gray-100 pb-6">
                  Give a name and a description to the proof request so you can identify it later.
                </h2>
                <div className="mb-6">
                  <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Name
                  </label>
                  <input
                    type="name"
                    id="name"
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>
                <div className="mb-6">
                  <label htmlFor="description" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Description
                  </label>
                  <input
                    type="description"
                    id="description"
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    required
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                  />
                </div>
                <div className="flex items-end justify-end">
                  <Button
                    id="continue"
                    onClick={() => setCurrentStep(3)}
                    label="Continue"
                    className="mt-4"
                    disabled={
                      description.length === 0 || name.length === 0
                    }
                  />
                </div>
              </>
            )
            || currentStep === 3 && (
              <>
                <h3 className="text-2xl font-bold tracking-tight text-white pb-6">
                  Json input
                </h3>
                <h2 className="tracking-tight text-gray-100 pb-6">
                  Insert a valid json input for model {modelOptions[selectedModelOption!].name}
                </h2>
                <JsonInputComponent jsonString={jsonInput} setJsonString={setJsonInput} />
                <div className="mt-4 flex flex-col items-end justify-end">
                  {
                    !isValidJson(jsonInput) && jsonInput.length > 0 &&
                    <p className="text-red-400 text-sm mb-1">Invalid JSON</p>
                  }
                  <Button
                    id="send"
                    type="submit"
                    label="Compute Proof"
                    disabled={
                      !isValidJson(jsonInput)
                    }
                  />
                </div>
              </>
            )
          }
        </div>
      </form>

      {/* <div className="relative px-6 pb-20 pt-24 sm:pt-32 lg:static lg:px-8 lg:py-40">
          <div className="mx-auto max-w-xl lg:mx-0 lg:max-w-lg">
            <h3 className="text-2xl  font-bold tracking-tight text-white">
              Proof Result:
            </h3>
            {proof && (
              <p className="mt-6 text-xs text-gray-300">
                {JSON.stringify(
                  JSON.parse(Buffer.from(proof, "base64").toString("utf-8")),
                  null,
                  2,
                )}
              </p>
            )}
          </div>
        </div> */}
    </div>
  );
}
