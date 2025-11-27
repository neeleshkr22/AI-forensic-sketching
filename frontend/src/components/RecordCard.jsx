import { useNavigate } from 'react-router-dom'
import { User, Trash2, Edit } from 'lucide-react'
import toast from 'react-hot-toast'
import { recordsAPI } from '../services/api'

export default function RecordCard({ record, onDeleted }) {
  const navigate = useNavigate()

  const handleDelete = async (e) => {
    e.stopPropagation()
    
    if (!confirm(`Are you sure you want to delete ${record.name}?`)) {
      return
    }

    try {
      await recordsAPI.delete(record.record_id)
      toast.success('Record deleted')
      onDeleted()
    } catch (error) {
      toast.error('Failed to delete record')
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-red-500/20 text-red-300 border border-red-400/30'
      case 'caught': return 'bg-green-500/20 text-green-300 border border-green-400/30'
      case 'inactive': return 'bg-gray-500/20 text-gray-300 border border-gray-400/30'
      default: return 'bg-gray-500/20 text-gray-300 border border-gray-400/30'
    }
  }

  return (
    <div
      onClick={() => navigate(`/records/${record.record_id}`)}
      className="glass rounded-2xl shadow-2xl hover:shadow-cyan-500/20 hover:scale-[1.02] hover:-translate-y-1 transition-all duration-300 cursor-pointer overflow-hidden"
    >
      {/* Photo */}
      <div className="aspect-square bg-gray-900/50">
        {record.photo_url ? (
          <img
            src={recordsAPI.getPhoto(record.record_id)}
            alt={record.name}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.target.style.display = 'none'
            }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <User className="w-20 h-20 text-gray-600" />
          </div>
        )}
      </div>

      {/* Info */}
      <div className="p-4">
        <div className="flex justify-between items-start mb-3">
          <div>
            <h3 className="text-lg font-bold text-gray-100">{record.name}</h3>
            <p className="text-sm text-gray-400">ID: {record.record_id.substring(0, 8)}</p>
          </div>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(record.status)}`}>
            {record.status}
          </span>
        </div>

        <div className="text-sm text-gray-300 space-y-1 mb-4">
          {record.age && <p>Age: {record.age}</p>}
          {record.gender && <p>Gender: {record.gender}</p>}
          {record.crime_type && <p>Crime: {record.crime_type}</p>}
        </div>

        <div className="flex space-x-2">
          <button
            onClick={(e) => {
              e.stopPropagation()
              navigate(`/records/${record.record_id}`)
            }}
            className="flex-1 btn-secondary text-sm py-2"
          >
            View Details
          </button>
          <button
            onClick={handleDelete}
            className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
