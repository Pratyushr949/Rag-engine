import React, { useState, useEffect, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import axios from 'axios';

const KnowledgeGraphViewer = ({ documentFilename }) => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const fgRef = useRef();

  useEffect(() => {
    if (!documentFilename) return;

    const fetchGraphData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get(`http://localhost:8000/api/network/${documentFilename}`);
        const data = response.data;
        setGraphData({
          nodes: data.nodes,
          links: data.links
        });
      } catch (err) {
        console.error("Failed to load graph data", err);
        setError("Failed to load graph data for this document.");
      } finally {
        setLoading(false);
      }
    };

    fetchGraphData();
  }, [documentFilename]);

  const handleNodeClick = (node) => {
    setSelectedNode(node);
    setSelectedEdge(null); // Clear edge selection
  };

  const handleEdgeClick = (link) => {
    setSelectedEdge(link);
    setSelectedNode(null); // Clear node selection
  };

  const handleBackgroundClick = () => {
    setSelectedNode(null);
    setSelectedEdge(null);
  };

  if (loading) return <div className="p-4 text-gray-500">Loading graph...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;
  if (!graphData.nodes.length) return <div className="p-4 text-gray-500">No graph data available. Please select a document.</div>;

  return (
    <div className="flex h-[600px] w-full relative bg-gray-900 border border-gray-700 rounded-lg overflow-hidden">
      {/* Graph Area */}
      <div className="flex-1" onClick={handleBackgroundClick}>
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          nodeLabel="id"
          nodeColor={(node) => {
            const type = node.type || "Unknown";
            switch(type.toLowerCase()) {
              case "persons": return "#f87171"; // red
              case "organizations": return "#60a5fa"; // blue
              case "companies": return "#3b82f6"; // blue
              case "locations": return "#34d399"; // green
              case "events": return "#fbbf24"; // yellow
              default: return "#9ca3af"; // gray
            }
          }}
          nodeVal={(node) => node.val ? Math.max(1, node.val * 20) : 3}
          linkColor={() => "#4b5563"} // gray-600
          linkDirectionalArrowLength={3.5}
          linkDirectionalArrowRelPos={1}
          linkWidth={(link) => selectedEdge && link === selectedEdge ? 3 : 1}
          onNodeClick={handleNodeClick}
          onLinkClick={handleEdgeClick}
          onBackgroundClick={handleBackgroundClick}
        />
      </div>

      {/* Side Panel for Metadata */}
      {(selectedNode || selectedEdge) && (
        <div className="absolute right-0 top-0 w-80 h-full bg-gray-800 text-gray-200 border-l border-gray-700 p-4 overflow-y-auto shadow-xl z-10">
          <h3 className="text-lg font-bold mb-4 border-b border-gray-600 pb-2">
            {selectedNode ? "Node Details" : "Relationship Details"}
          </h3>
          
          {selectedNode && (
            <div className="space-y-3">
              <div>
                <span className="text-gray-400 text-sm block">Entity</span>
                <span className="font-semibold text-white">{selectedNode.id}</span>
              </div>
              <div>
                <span className="text-gray-400 text-sm block">Type</span>
                <span className="font-semibold text-blue-400">{selectedNode.type || "Unknown"}</span>
              </div>
              {selectedNode.val && (
                <div>
                  <span className="text-gray-400 text-sm block">Centrality</span>
                  <span className="text-sm">{selectedNode.val.toFixed(4)}</span>
                </div>
              )}
            </div>
          )}

          {selectedEdge && (
            <div className="space-y-3">
              <div>
                <span className="text-gray-400 text-sm block">Relationship Type</span>
                <span className="font-semibold text-green-400">{selectedEdge.label || selectedEdge.type || "Unknown"}</span>
              </div>
              <div>
                <span className="text-gray-400 text-sm block">Source</span>
                <span className="text-white text-sm">{typeof selectedEdge.source === 'object' ? selectedEdge.source.id : selectedEdge.source}</span>
              </div>
              <div>
                <span className="text-gray-400 text-sm block">Target</span>
                <span className="text-white text-sm">{typeof selectedEdge.target === 'object' ? selectedEdge.target.id : selectedEdge.target}</span>
              </div>
            </div>
          )}
          
          <button 
            className="mt-6 w-full py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm transition-colors"
            onClick={handleBackgroundClick}
          >
            Close Panel
          </button>
        </div>
      )}
    </div>
  );
};

export default KnowledgeGraphViewer;
