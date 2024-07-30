import dynamic from 'next/dynamic';
import React, { useState, useEffect } from 'react';

// Dynamically import the Monaco Editor to ensure it works with Next.js
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

interface JsonInputComponentProps {
  jsonString: string;
  setJsonString: (value: string) => void;
}

const JsonInputComponent: React.FC<JsonInputComponentProps> = ({ jsonString, setJsonString }) => {
  const handleJsonChange = (value: string | undefined) => {
    if (value !== undefined) {
      setJsonString(value);
    }
  };

  return (
    <div>
      <h3>JSON Input</h3>
      <MonacoEditor
        height="400px"
        defaultLanguage="json"
        theme="vs-dark"
        value={jsonString}
        onChange={handleJsonChange}
        options={{
          selectOnLineNumbers: true,
          automaticLayout: true,
        }}
      />
    </div>
  );
};

export default JsonInputComponent;
