import React, { useState } from 'react';
import KnowledgeGraphViewer from '../components/KnowledgeGraphViewer';
import { Search } from 'lucide-react';

export default function GraphPage() {
  const [filenameInput, setFilenameInput] = useState('');
  const [activeDocument, setActiveDocument] = useState('global');

  const handleSearch = (e) => {
    e.preventDefault();
    if (filenameInput.trim()) {
      setActiveDocument(filenameInput.trim());
    }
  };

  const loadGlobal = () => {
    setActiveDocument('global');
    setFilenameInput('');
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 h-[calc(100vh-100px)] flex flex-col">
      <div className="mb-6 animate-fade-in flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Knowledge Graph</h1>
          <p className="text-muted-foreground">Visualize entities and relationships extracted from your documents.</p>
          
          <form onSubmit={handleSearch} className="mt-4 flex max-w-md">
            <input
              type="text"
              placeholder="Enter document filename (or use global)"
              className="flex-1 bg-background border border-input rounded-l-md px-4 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              value={filenameInput}
              onChange={(e) => setFilenameInput(e.target.value)}
            />
            <button
              type="submit"
              className="bg-primary text-primary-foreground px-4 py-2 hover:bg-primary/90 flex items-center"
            >
              <Search className="w-4 h-4 mr-2" />
              Load
            </button>
            <button
              type="button"
              onClick={loadGlobal}
              className="bg-secondary text-secondary-foreground px-4 py-2 rounded-r-md hover:bg-secondary/90 border-l border-border"
            >
              Load Global
            </button>
          </form>
        </div>
      </div>

      <div className="flex-1 min-h-[500px] animate-fade-in delay-100">
        <KnowledgeGraphViewer documentFilename={activeDocument} />
      </div>
    </div>
  );
}
