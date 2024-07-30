"use client";

import { useState } from "react";
import { twMerge } from 'tailwind-merge';
import Button from "@/components/Button";
import { useChain } from "@/contexts/Chain";
import JsonInputComponent from "@/components/JsonInputComponent";
import { isValidJson } from "../../../utils/json";

const modelOptions = [
  {
    name: "Ladybird model",
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
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState("");
  const [proof, setProof] = useState("");

  const { fetchEscrowBalance, escrowBalance } = useChain();

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    setProof("");

    console.log("tamo aqui")
    console.log("test", isValidJson(jsonInput))

    // setLogs(`Creating a new job...`);

    // const clientId = localStorage.getItem("clientId");
    // const job = await callHub("/jobs", "POST", {
    //   clientId,
    //   r1csScript: form.r1csScript,
    // });

    // if (!job.success) {
    //   setLogs((logs) => `${logs}Job not created: ${job.error}`);
    //   setLoading(false);
    //   return;
    // }

    // setLogs(
    //   (logs) =>
    //     `${logs}Job ${
    //       job.data.id
    //     } created.\nEncrypting witness using Worker public key:\n${Buffer.from(
    //       job.data.encryptKey,
    //       "base64",
    //     ).toString("utf-8")}\n`,
    // );

    // const encryptResponse = await fetch("/api/encrypt", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({
    //     base64EnclavePublicKey: job.data.encryptKey,
    //     base64Witness: form.witness,
    //   }),
    // });
    // const { base64EncryptedWitness, base64EncryptedAesKey, base64AesIv } =
    //   await encryptResponse.json();

    // setLogs((logs) => `${logs}Witness encrypted succesfuly.\nStarting job...`);

    // await callHub("/jobs/start", "POST", {
    //   jobId: job.data.id,
    //   witness: base64EncryptedWitness,
    //   aesKey: base64EncryptedAesKey,
    //   aesIv: base64AesIv,
    // });

    // setLogs((logs) => `${logs}Done.\nWaiting for proof...`);

    // const jobInterval = setInterval(async () => {
    //   const jobInfo = await callHub(`/jobs/${job.data.id}`, "GET");
    //   if (jobInfo && jobInfo.data.proof) {
    //     setProof(jobInfo.data.proof);
    //     clearInterval(jobInterval);

    //     setLogs((logs) => `${logs}Done.`);
    //     fetchEscrowBalance();
    //     setLoading(false);
    //   }
    // }, 3000);
  };

  const callHub = async (url: string, method: string, body?: any) => {
    const apiKey = localStorage.getItem("apiKey");

    const options = {
      method: method,
      headers: {
        "Content-Type": "application/json",
        api_key: apiKey!,
      },
    } as RequestInit;

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_HUB_URL}${url}`,
      options,
    );

    const data = await response.json();

    if (!response.ok) {
      if (response.status === 400) {
        return {
          success: false,
          error: data.error,
        };
      }

      throw new Error("Failed to fetch data from the server.");
    }

    return {
      success: true,
      data,
    };
  };

  return (
    <div className="relative bg-gray-900 h-screen">
      {/* <div className="absolute inset-y-0 right-0 -z-10 w-full overflow-hidden ring-1 ring-white/5">
        <svg
          className="absolute inset-0 h-full w-full stroke-gray-700 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]"
          aria-hidden="true"
        >
          <defs>
            <pattern
              id="54f88622-e7f8-4f1d-aaf9-c2f5e46dd1f2"
              width={200}
              height={200}
              x="100%"
              y={-1}
              patternUnits="userSpaceOnUse"
            >
              <path d="M130 200V.5M.5 .5H200" fill="none" />
            </pattern>
          </defs>
          <svg x="100%" y={-1} className="overflow-visible fill-gray-800/20">
            <path d="M-470.5 0h201v201h-201Z" strokeWidth={0} />
          </svg>
          <rect
            width="100%"
            height="100%"
            strokeWidth={0}
            fill="url(#54f88622-e7f8-4f1d-aaf9-c2f5e46dd1f2)"
          />
        </svg>
        <div
          className="absolute -left-56 top-[calc(100%-13rem)] transform-gpu blur-3xl lg:left-[max(-14rem,calc(100%-59rem))] lg:top-[calc(50%-7rem)]"
          aria-hidden="true"
        >
          <div
            className="aspect-[1155/678] w-[72.1875rem] bg-gradient-to-br from-[#80caff] to-[#4f46e5] opacity-20"
            style={{
              clipPath:
                "polygon(74.1% 56.1%, 100% 38.6%, 97.5% 73.3%, 85.5% 100%, 80.7% 98.2%, 72.5% 67.7%, 60.2% 37.8%, 52.4% 32.2%, 47.5% 41.9%, 45.2% 65.8%, 27.5% 23.5%, 0.1% 35.4%, 17.9% 0.1%, 27.6% 23.5%, 76.1% 2.6%, 74.1% 56.1%)",
            }}
          />
        </div>
      </div> */}

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
          {logs && (
            <div className="mt-3 text-white">
              <h3 className="text-2xl font-bold tracking-tight text-white">
                Logs:
              </h3>
              <pre className="text-xs leading-8 text-gray-300">{logs}</pre>
            </div>
          )}
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
