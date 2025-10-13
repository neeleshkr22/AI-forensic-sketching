import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import SketchCreator from './pages/SketchCreator'
import SearchResults from './pages/SearchResults'
import RecordManagement from './pages/RecordManagement'
import RecordDetail from './pages/RecordDetail'

function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/sketch" element={<SketchCreator />} />
          <Route path="/results" element={<SearchResults />} />
          <Route path="/records" element={<RecordManagement />} />
          <Route path="/records/:id" element={<RecordDetail />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
