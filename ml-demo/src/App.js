import { useState } from 'react';

function ImageTextRecognizer() {
    const [image, setImage] = useState(null);
    const [result, setResult] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImage(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const processImage = async () => {
        if (!image) return;

        setIsLoading(true);

        try {
            // Replace this with actual ML model API call
            const mockResults = await mockTextRecognition(image);
            setResult(mockResults);
        } catch (error) {
            console.error("Recognition error:", error);
            setResult("Error processing image");
        } finally {
            setIsLoading(false);
        }
    };

    // Mock function - replace with your actual model integration
    const mockTextRecognition = async (imageData) => {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("Sample recognized text: ABC123\nConfidence: 95%");
            }, 1500);
        });
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