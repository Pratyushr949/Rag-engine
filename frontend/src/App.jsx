import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/layout/Layout";
import UploadPage from "./pages/UploadPage";
import ChatPage from "./pages/ChatPage";
import GraphPage from "./pages/GraphPage";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/chat" replace />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/graph" element={<GraphPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
