import { useState } from 'react'
import appLogo from './assets/app_icon.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [preview, setPreview] = useState(null);
  const [fileType, setFileType] = useState('image'); // 'image' or 'pdf'
  const [result, setResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (fileType === 'image') {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    } else {
      setPreview(URL.createObjectURL(file));
    }

    console.log("Selected file:", file);
  };

  // const processImage = async () => {
  //   if (!previewImage) return;
  //
  //   setIsLoading(true);
  //
  //   try {
  //     // Replace this with actual ML model API call
  //     const mockResults = await mockTextRecognition(image);
  //     setResult(mockResults);
  //   } catch (error) {
  //     console.error("Recognition error:", error);
  //     setResult("Error processing image");
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };
  //
  // // Mock function - replace with actual model integration
  // const mockTextRecognition = async (imageData) => {
  //   return new Promise((resolve) => {
  //     setTimeout(() => {
  //       resolve("Sample recognized text: ABC123\nConfidence: 95%");
  //     }, 1500);
  //   });
  // };

  return (
    <>
      <div>
        <a href="https://github.com/Rualin/RDR" target="_blank">
          <img src={appLogo} className="logo" alt="App logo" />
        </a>
      </div>
      <h1>Распознавание врачебных заключений</h1>


      <div className="file-upload-container">
        {/* File type selector */}
        <div className="file-type-selector">
          <button
            className={`selector-btn ${fileType === 'image' ? 'active' : ''}`}
            onClick={() => {
              setFileType('image');
              setPreview(null);
            }}
          >
            <svg className="selector-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Изображение
          </button>
          <button
            className={`selector-btn ${fileType === 'pdf' ? 'active' : ''}`}
            onClick={() => {
              setFileType('pdf');
              setPreview(null);
            }}
          >
            <svg className="selector-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            PDF
          </button>
        </div>

        {/* File input */}
        <input
          type="file"
          id="fileUpload"
          accept={fileType === 'image' ? 'image/*' : 'application/pdf'}
          onChange={handleFileUpload}
          className="hidden-input"
        />

        {/* Upload button */}
        <label htmlFor="fileUpload" className="upload-button">
          <svg className="upload-icon" /* ... your SVG ... */ />
          Загрузить {fileType === 'image' ? 'Изображение' : 'PDF'}
        </label>

        {/* Preview area */}
        {preview && (
          <div className="preview-container">
            {fileType === 'image' ? (
              <img src={preview} alt="Preview" className="preview-content" />
            ) : (
              <iframe
                src={preview}
                className="preview-content pdf-preview"
                title="PDF Preview"
              />
            )}
          </div>
        )}

        {/* Status */}
        <div className="file-status">
          {preview ? `${fileType.toUpperCase()} loaded` : 'No file selected'}
        </div>
      </div>


      <p className="app info">
        v0.2
      </p>
    </>
  )
}

export default App
