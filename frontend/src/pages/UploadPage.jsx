import { useState, useRef } from "react";
import { UploadCloud, File, CheckCircle2, AlertCircle } from "lucide-react";
import { uploadDocument } from "../services/api";
import { cn } from "../utils/cn";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0];
    validateAndSetFile(selected);
  };

  const validateAndSetFile = (selectedFile) => {
    setError(null);
    setResult(null);
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
    } else if (selectedFile) {
      setError("Please select a valid PDF file.");
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files?.[0];
    validateAndSetFile(droppedFile);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setIsUploading(true);
    setUploadProgress(0);
    setError(null);
    
    try {
      const data = await uploadDocument(file, (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(percentCompleted);
      });
      setResult(data);
      setFile(null); // Clear after success
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "An error occurred during upload.");
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <div className="mb-10 text-center animate-fade-in">
        <h1 className="text-3xl font-bold tracking-tight mb-2">Knowledge Base Setup</h1>
        <p className="text-muted-foreground">Upload your PDF documents to index them into the RAG engine.</p>
      </div>
      
      <div 
        className={cn(
          "glass-dark rounded-2xl p-10 transition-all duration-300 flex flex-col items-center justify-center border-2 border-dashed relative overflow-hidden group",
          isDragging ? "border-primary bg-primary/5 scale-[1.02]" : "border-border/60 hover:border-primary/50 hover:bg-muted/30"
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="absolute inset-0 bg-gradient-to-tr from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
        
        <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mb-6">
          <UploadCloud className={cn("w-10 h-10 text-primary transition-transform duration-300", isDragging && "scale-110 -translate-y-1")} />
        </div>
        
        <h3 className="text-xl font-semibold mb-2">Drop your PDF here</h3>
        <p className="text-muted-foreground mb-6 text-center max-w-sm">
          Drag and drop your file, or click the button below to browse your computer.
        </p>
        
        <input 
          type="file" 
          accept=".pdf" 
          className="hidden" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
        />
        
        <button 
          onClick={() => fileInputRef.current?.click()}
          className="px-6 py-2.5 bg-secondary text-secondary-foreground font-medium rounded-lg hover:bg-secondary/80 transition-colors shadow-sm"
        >
          Select File
        </button>
      </div>
      
      {file && (
        <div className="mt-6 glass rounded-xl p-4 flex items-center justify-between animate-fade-in border border-primary/20 bg-primary/5">
          <div className="flex items-center space-x-3 overflow-hidden">
            <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center shrink-0">
              <File className="w-5 h-5 text-primary" />
            </div>
            <div className="min-w-0">
              <p className="font-medium truncate">{file.name}</p>
              <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>
          <button 
            onClick={handleUpload}
            disabled={isUploading}
            className="ml-4 px-5 py-2 bg-primary text-primary-foreground font-medium rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-70 shadow-md shrink-0 flex items-center"
          >
            {isUploading ? (
              <>
                <div className="w-4 h-4 rounded-full border-2 border-primary-foreground/30 border-t-primary-foreground animate-spin mr-2" />
                Processing...
              </>
            ) : "Upload & Index"}
          </button>
        </div>
      )}
      
      {isUploading && uploadProgress > 0 && uploadProgress < 100 && (
        <div className="mt-4 animate-fade-in">
          <div className="flex justify-between text-xs text-muted-foreground mb-1">
            <span>Uploading...</span>
            <span>{uploadProgress}%</span>
          </div>
          <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
            <div 
              className="bg-primary h-2 rounded-full transition-all duration-300 ease-out" 
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}
      
      {error && (
        <div className="mt-6 p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive flex items-start animate-fade-in">
          <AlertCircle className="w-5 h-5 mr-3 shrink-0 mt-0.5" />
          <p className="text-sm font-medium">{error}</p>
        </div>
      )}
      
      {result && (
        <div className="mt-6 p-6 rounded-xl bg-green-500/10 border border-green-500/20 flex items-start animate-fade-in">
          <CheckCircle2 className="w-6 h-6 text-green-500 mr-4 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-green-500 mb-1">Upload Successful</h4>
            <p className="text-sm text-foreground/80 mb-3">{result.message}</p>
            
            <div className="flex space-x-6 text-sm">
              <div className="flex flex-col">
                <span className="text-muted-foreground text-xs uppercase font-semibold">Pages</span>
                <span className="font-medium">{result.pages}</span>
              </div>
              <div className="flex flex-col">
                <span className="text-muted-foreground text-xs uppercase font-semibold">Chunks Indexed</span>
                <span className="font-medium">{result.chunks}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
