import { useState } from 'react';

function ImageTextRecognizer() {
    const [image, setImage] = useState(null);
    const [imageFile, setImageFile] = useState(null); // Store the actual file for API
    const [result, setResult] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const API_URL = 'https://your-ml-api-endpoint.com/predict'; // Replace with your API endpoint

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImageFile(file); // Store the file for API submission
            const reader = new FileReader();
            reader.onloadend = () => {
                setImage(reader.result);
            };
            reader.readAsDataURL(file);
            setError(null); // Reset error on new upload
            setResult(''); // Clear previous results
        }
    };

    // 2. Process image with real API
    const processImage = async () => {
        if (!imageFile) return;

        setIsLoading(true);
        setError(null);

        try {
            // Create FormData for the API request
            const formData = new FormData();
            formData.append('image', imageFile);

            // API call
            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData,
                headers: {
                    // Include API key if needed
                    // 'Authorization': `Bearer ${API_KEY}`,
                },
            });

            if (!response.ok) {
                throw new Error(`API request failed with status ${response.status}`);
            }

            const data = await response.json();

            // Format the result based on your API response structure
            setResult(formatApiResponse(data));

        } catch (error) {
            console.error("Recognition error:", error);
            setError("Failed to process image. Please try again.");
            setResult('');
        } finally {
            setIsLoading(false);
        }
    };

    // Format the API response for display
    const formatApiResponse = (apiData) => {
        if (apiData.text) {
            return `Recognized text: ${apiData.text}\n}`;
        }
        return JSON.stringify(apiData, null, 2); // Fallback to raw JSON
    };

    return (
        <div className="container mt-5">
            <h2 className="mb-4">Image Text Recognition</h2>

            <div className="row">
                <div className="col-md-6">
                    {/* Image Upload */}
                    <div className="mb-3">
                        <label htmlFor="imageUpload" className="form-label">
                            Upload Image
                        </label>
                        <input
                            type="file"
                            className="form-control"
                            id="imageUpload"
                            accept="image/*"
                            onChange={handleImageUpload}
                            disabled={isLoading}
                        />
                    </div>

                    {/* Preview */}
                    {image && (
                        <div className="mb-3">
                            <h5>Image Preview:</h5>
                            <img
                                src={image}
                                alt="Preview"
                                className="img-fluid rounded"
                                style={{ maxHeight: '300px' }}
                            />
                        </div>
                    )}

                    {/* Process Button */}
                    <button
                        className="btn btn-primary"
                        onClick={processImage}
                        disabled={!image || isLoading}
                    >
                        {isLoading ? (
                            <>
                                <span className="spinner-border spinner-border-sm" role="status"></span>
                                Processing...
                            </>
                        ) : (
                            'Recognize Text'
                        )}
                    </button>

                    {/* Error message */}
                    {error && (
                        <div className="alert alert-danger mt-3">
                            {error}
                        </div>
                    )}
                </div>

                <div className="col-md-6">
                    {/* Results */}
                    <div className="card">
                        <div className="card-header">Recognition Results</div>
                        <div className="card-body">
                            {result ? (
                                <pre className="mb-0">{result}</pre>
                            ) : (
                                <p className="text-muted mb-0">
                                    {image ? 'Click "Recognize Text" to process' : 'Upload an image first'}
                                </p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ImageTextRecognizer;