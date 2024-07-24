import dynamic from 'next/dynamic';
import React, { useState, useEffect } from 'react';

// Dynamically import the Monaco Editor to ensure it works with Next.js
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

interface JsonInputComponentProps {
  jsonString: string;
}

const JsonInputComponent: React.FC<JsonInputComponentProps> = ({ jsonString }) => {
  const [jsonData, setJsonData] = useState<string>(jsonString);

  useEffect(() => {
    setJsonData(jsonString);
  }, [jsonString]);

  // Function to handle changes in the Monaco Editor
  const handleJsonChange = (value: string | undefined) => {
    if (value !== undefined) {
      try {
        JSON.parse(value); // Validate JSON
        setJsonData(value); // Update state if valid
      } catch (e) {
        console.error('Invalid JSON');
      }
    }
  };

  return (
    <div>
      <h3>JSON Input</h3>
      <MonacoEditor
        height="400px"
        defaultLanguage="json"
        theme="vs-dark"
        value={jsonData}
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
