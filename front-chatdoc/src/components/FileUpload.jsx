import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import styled from 'styled-components';

const DropzoneContainer = styled.div`
  border: 2px dashed ${({ $isDragActive, $hasFile }) =>
    $isDragActive ? '#007bff' : $hasFile ? '#4caf50' : '#ccc'};
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  background-color: ${({ $isDragActive }) =>
    $isDragActive ? 'rgba(0, 123, 255, 0.05)' : 'transparent'};
  transition: border-color 0.2s ease;
  margin-bottom: 20px;

  &:hover {
    border-color: ${({ $hasFile }) => ($hasFile ? '#4caf50' : '#007bff')};
  }
`;

const FileUpload = ({ onFileUpload, currentFile, onUploadComplete }) => {

  const handleUpload = async (file) => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      console.log("Starting upload...");

      const response = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      console.log("Upload response status:", response.status);

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      // IMPORTANT:
      // Backend returned 200, so mark upload as complete.
      onUploadComplete(true);

      console.log("Upload completed successfully");

    } catch (error) {
      console.error("Upload Error:", error);
      onUploadComplete(false);
    }
  };

  const onDrop = useCallback(
    (acceptedFiles) => {
      const file = acceptedFiles[0];

      if (file) {
        console.log("File selected:", file.name);

        // Show selected file
        onFileUpload(file);

        // Disable chat while uploading
        onUploadComplete(false);

        // Upload to backend
        handleUpload(file);
      }
    },
    [onFileUpload, onUploadComplete]
  );

  const removeFile = useCallback(
    (e) => {
      e.stopPropagation();

      onFileUpload(null);
      onUploadComplete(false);
    },
    [onFileUpload, onUploadComplete]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    onDrop,
    disabled: !!currentFile,
  });

  return (
    <DropzoneContainer
      {...getRootProps()}
      $isDragActive={isDragActive}
      $hasFile={!!currentFile}
    >
      <input {...getInputProps()} />

      {currentFile ? (
        <div>
          <span>{currentFile.name}</span>
          <button onClick={removeFile}>Remove</button>
        </div>
      ) : (
        <p>
          {isDragActive
            ? 'Drop the PDF here...'
            : "Drag 'n' drop a PDF here, or click to select"}
        </p>
      )}
    </DropzoneContainer>
  );
};

export default FileUpload;