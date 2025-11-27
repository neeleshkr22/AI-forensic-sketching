import { useState, useEffect } from 'react'
import { Plus, Search, Filter } from 'lucide-react'
import toast from 'react-hot-toast'
import { recordsAPI } from '../services/api'
import RecordCard from '../components/RecordCard'
import AddRecordModal from '../components/AddRecordModal'

export default function RecordManagement() {
  const [records, setRecords] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [stats, setStats] = useState(null)

  useEffect(() => {
    loadRecords()
    loadStats()
  }, [statusFilter])

  const loadRecords = async () => {
    setIsLoading(true)
    try {
      const filters = statusFilter !== 'all' ? { status: statusFilter } : {}
      const result = await recordsAPI.getAll(0, 100, filters)
      setRecords(result.records || [])
    } catch (error) {
      toast.error('Failed to load records')
    } finally {
      setIsLoading(false)
    }
  }

  const loadStats = async () => {
    try {
      const result = await recordsAPI.getStats()
      setStats(result.stats)
    } catch (error) {
      console.error('Failed to load stats')
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadRecords()
      return
    }

    try {
      const result = await recordsAPI.search(searchQuery)
      setRecords(result.records || [])
    } catch (error) {
      toast.error('Search failed')
    }
  }

  const handleRecordAdded = () => {
    setShowAddModal(false)
    loadRecords()
    loadStats()
    toast.success('Record added successfully!')
  }

  const handleRecordDeleted = () => {
    loadRecords()
    loadStats()
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Criminal Records
          </h1>
          <p className="text-lg text-gray-300">
            Manage and search criminal database
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Add Record</span>
        </button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <div className="glass rounded-2xl shadow-2xl p-6 border border-cyan-500/30">
            <h3 className="text-sm font-medium text-gray-300 mb-1">Total Records</h3>
            <p className="text-3xl font-bold text-cyan-400">{stats.total_records}</p>
          </div>
          <div className="glass rounded-2xl shadow-2xl p-6 border border-green-500/30">
            <h3 className="text-sm font-medium text-gray-300 mb-1">Active</h3>
            <p className="text-3xl font-bold text-green-400">{stats.active}</p>
          </div>
          <div className="glass rounded-2xl shadow-2xl p-6 border border-blue-500/30">
            <h3 className="text-sm font-medium text-gray-300 mb-1">Caught</h3>
            <p className="text-3xl font-bold text-blue-400">{stats.caught}</p>
          </div>
          <div className="glass rounded-2xl shadow-2xl p-6 border border-gray-500/30">
            <h3 className="text-sm font-medium text-gray-300 mb-1">Inactive</h3>
            <p className="text-3xl font-bold text-gray-400">{stats.inactive}</p>
          </div>
        </div>
      )}

      {/* Search and Filter */}
      <div className="glass rounded-2xl shadow-2xl p-6 mb-8">
        <div className="grid md:grid-cols-2 gap-4">
          <div className="flex space-x-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Search by name..."
              className="input-field flex-1"
            />
            <button
              onClick={handleSearch}
              className="btn-primary flex items-center space-x-2"
            >
              <Search className="w-5 h-5" />
              <span>Search</span>
            </button>
          </div>

          <div className="flex items-center space-x-2">
            <Filter className="w-5 h-5 text-cyan-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input-field"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="caught">Caught</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>
      </div>

      {/* Records Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="loading-spinner mx-auto" />
        </div>
      ) : records.length === 0 ? (
        <div className="glass rounded-2xl p-12 text-center">
          <p className="text-gray-300">No records found</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {records.map((record) => (
            <RecordCard
              key={record.record_id}
              record={record}
              onDeleted={handleRecordDeleted}
            />
          ))}
        </div>
      )}

      {/* Add Record Modal */}
      {showAddModal && (
        <AddRecordModal
          onClose={() => setShowAddModal(false)}
          onSuccess={handleRecordAdded}
        />
      )}
    </div>
  )
}
