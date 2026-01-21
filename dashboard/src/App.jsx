import React, { useState, useEffect } from 'react';
import { 
  Cpu, 
  HardDrive, 
  Activity, 
  Zap, 
  Server, 
  Brain, 
  Terminal,
  Globe,
  Settings,
  Play,
  Square,
  RefreshCw,
  CheckCircle,
  XCircle,
  AlertCircle,
  MessageSquare,
  Code,
  Layers,
  Monitor,
  Thermometer
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

// Simulated data for demo
const generateGPUData = () => {
  const data = [];
  for (let i = 0; i < 20; i++) {
    data.push({
      time: `${i}s`,
      usage: Math.floor(Math.random() * 40) + 30,
      memory: Math.floor(Math.random() * 30) + 50,
      temp: Math.floor(Math.random() * 15) + 55,
    });
  }
  return data;
};

// Status Badge Component
const StatusBadge = ({ status }) => {
  const styles = {
    running: 'bg-green-500/20 text-green-400 border-green-500/30',
    stopped: 'bg-red-500/20 text-red-400 border-red-500/30',
    loading: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  };
  
  const icons = {
    running: <CheckCircle className="w-3 h-3" />,
    stopped: <XCircle className="w-3 h-3" />,
    loading: <AlertCircle className="w-3 h-3" />,
  };

  return (
    <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs border ${styles[status]}`}>
      {icons[status]}
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

// Stat Card Component
const StatCard = ({ icon: Icon, title, value, subtitle, color = 'blue' }) => {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
  };

  return (
    <div className="glass rounded-xl p-4 hover:scale-105 transition-transform duration-300">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm">{title}</p>
          <p className="text-2xl font-bold text-white mt-1">{value}</p>
          {subtitle && <p className="text-gray-500 text-xs mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-lg bg-gradient-to-br ${colors[color]}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );
};

// Service Card Component
const ServiceCard = ({ name, status, port, icon: Icon, onStart, onStop }) => {
  return (
    <div className="glass rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-blue-500/20">
            <Icon className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h3 className="text-white font-medium">{name}</h3>
            <p className="text-gray-500 text-xs">Port: {port}</p>
          </div>
        </div>
        <StatusBadge status={status} />
      </div>
      <div className="flex gap-2">
        <button 
          onClick={onStart}
          disabled={status === 'running'}
          className="flex-1 flex items-center justify-center gap-1 py-2 rounded-lg bg-green-500/20 text-green-400 hover:bg-green-500/30 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
        >
          <Play className="w-4 h-4" /> Start
        </button>
        <button 
          onClick={onStop}
          disabled={status === 'stopped'}
          className="flex-1 flex items-center justify-center gap-1 py-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
        >
          <Square className="w-4 h-4" /> Stop
        </button>
      </div>
    </div>
  );
};

// Model Card Component
const ModelCard = ({ name, size, status, vram }) => {
  return (
    <div className="glass rounded-lg p-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-purple-500/20">
          <Brain className="w-4 h-4 text-purple-400" />
        </div>
        <div>
          <h4 className="text-white text-sm font-medium">{name}</h4>
          <p className="text-gray-500 text-xs">{size} • {vram} VRAM</p>
        </div>
      </div>
      <StatusBadge status={status} />
    </div>
  );
};

// Quick Action Button
const QuickAction = ({ icon: Icon, label, onClick, color = 'blue' }) => {
  const colors = {
    blue: 'bg-blue-500/20 text-blue-400 hover:bg-blue-500/30',
    green: 'bg-green-500/20 text-green-400 hover:bg-green-500/30',
    purple: 'bg-purple-500/20 text-purple-400 hover:bg-purple-500/30',
    orange: 'bg-orange-500/20 text-orange-400 hover:bg-orange-500/30',
  };

  return (
    <button 
      onClick={onClick}
      className={`flex flex-col items-center gap-2 p-4 rounded-xl ${colors[color]} transition-colors`}
    >
      <Icon className="w-6 h-6" />
      <span className="text-xs">{label}</span>
    </button>
  );
};

// Main App Component
function App() {
  const [gpuData, setGpuData] = useState(generateGPUData());
  const [services, setServices] = useState({
    openhands: 'running',
    ollama: 'running',
    browser: 'stopped',
  });
  const [gpuStats, setGpuStats] = useState({
    usage: 45,
    memory: 12.4,
    totalMemory: 24,
    temp: 62,
    power: 180,
  });

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setGpuData(prev => {
        const newData = [...prev.slice(1), {
          time: `${parseInt(prev[prev.length - 1].time) + 1}s`,
          usage: Math.floor(Math.random() * 40) + 30,
          memory: Math.floor(Math.random() * 30) + 50,
          temp: Math.floor(Math.random() * 15) + 55,
        }];
        return newData;
      });
      
      setGpuStats(prev => ({
        ...prev,
        usage: Math.floor(Math.random() * 40) + 30,
        memory: (Math.random() * 8 + 10).toFixed(1),
        temp: Math.floor(Math.random() * 15) + 55,
        power: Math.floor(Math.random() * 50) + 150,
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const toggleService = (service, action) => {
    setServices(prev => ({
      ...prev,
      [service]: action === 'start' ? 'loading' : 'loading'
    }));
    
    setTimeout(() => {
      setServices(prev => ({
        ...prev,
        [service]: action === 'start' ? 'running' : 'stopped'
      }));
    }, 1500);
  };

  return (
    <div className="min-h-screen p-6">
      {/* Header */}
      <header className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-4">
          <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 glow">
            <Layers className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">OpenHands Dashboard</h1>
            <p className="text-gray-400 text-sm">GPU-Accelerated AI Coding Assistant</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button className="p-2 rounded-lg glass hover:bg-white/10 transition-colors">
            <RefreshCw className="w-5 h-5 text-gray-400" />
          </button>
          <button className="p-2 rounded-lg glass hover:bg-white/10 transition-colors">
            <Settings className="w-5 h-5 text-gray-400" />
          </button>
        </div>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard 
          icon={Cpu} 
          title="GPU Usage" 
          value={`${gpuStats.usage}%`}
          subtitle="NVIDIA RTX 4090"
          color="blue"
        />
        <StatCard 
          icon={HardDrive} 
          title="VRAM Used" 
          value={`${gpuStats.memory} GB`}
          subtitle={`of ${gpuStats.totalMemory} GB`}
          color="purple"
        />
        <StatCard 
          icon={Thermometer} 
          title="Temperature" 
          value={`${gpuStats.temp}°C`}
          subtitle="Normal"
          color="orange"
        />
        <StatCard 
          icon={Zap} 
          title="Power Draw" 
          value={`${gpuStats.power}W`}
          subtitle="TDP: 450W"
          color="green"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* GPU Chart */}
        <div className="lg:col-span-2 glass rounded-xl p-6">
          <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-400" />
            GPU Performance
          </h2>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={gpuData}>
              <defs>
                <linearGradient id="colorUsage" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorMemory" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px'
                }}
              />
              <Area type="monotone" dataKey="usage" stroke="#3b82f6" fillOpacity={1} fill="url(#colorUsage)" name="GPU %" />
              <Area type="monotone" dataKey="memory" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorMemory)" name="Memory %" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Services */}
        <div className="glass rounded-xl p-6">
          <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
            <Server className="w-5 h-5 text-green-400" />
            Services
          </h2>
          <div className="space-y-3">
            <ServiceCard 
              name="OpenHands" 
              status={services.openhands}
              port="3000"
              icon={Layers}
              onStart={() => toggleService('openhands', 'start')}
              onStop={() => toggleService('openhands', 'stop')}
            />
            <ServiceCard 
              name="Ollama" 
              status={services.ollama}
              port="11434"
              icon={Brain}
              onStart={() => toggleService('ollama', 'start')}
              onStop={() => toggleService('ollama', 'stop')}
            />
            <ServiceCard 
              name="Browser" 
              status={services.browser}
              port="9222"
              icon={Globe}
              onStart={() => toggleService('browser', 'start')}
              onStop={() => toggleService('browser', 'stop')}
            />
          </div>
        </div>
      </div>

      {/* Models and Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Installed Models */}
        <div className="glass rounded-xl p-6">
          <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-400" />
            Installed Models
          </h2>
          <div className="space-y-2">
            <ModelCard 
              name="deepseek-coder-v2:16b" 
              size="9.0 GB" 
              status="running"
              vram="16 GB"
            />
            <ModelCard 
              name="deepseek-coder:6.7b" 
              size="3.8 GB" 
              status="stopped"
              vram="8 GB"
            />
            <ModelCard 
              name="llama3.1:8b" 
              size="4.7 GB" 
              status="stopped"
              vram="8 GB"
            />
          </div>
          <button className="w-full mt-4 py-2 rounded-lg border border-dashed border-gray-600 text-gray-400 hover:border-blue-500 hover:text-blue-400 transition-colors text-sm">
            + Pull New Model
          </button>
        </div>

        {/* Quick Actions */}
        <div className="glass rounded-xl p-6">
          <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-400" />
            Quick Actions
          </h2>
          <div className="grid grid-cols-4 gap-3">
            <QuickAction 
              icon={Globe} 
              label="Open UI" 
              color="blue"
              onClick={() => window.open('http://localhost:3000', '_blank')}
            />
            <QuickAction 
              icon={Terminal} 
              label="Terminal" 
              color="green"
              onClick={() => {}}
            />
            <QuickAction 
              icon={Code} 
              label="VS Code" 
              color="purple"
              onClick={() => {}}
            />
            <QuickAction 
              icon={MessageSquare} 
              label="Chat" 
              color="orange"
              onClick={() => {}}
            />
          </div>
          
          {/* Command Input */}
          <div className="mt-4">
            <label className="text-gray-400 text-sm mb-2 block">Quick Command</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                placeholder="docker compose up -d..."
                className="flex-1 bg-black/30 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
              />
              <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg text-white transition-colors">
                Run
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* System Info */}
      <div className="glass rounded-xl p-6">
        <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
          <Monitor className="w-5 h-5 text-cyan-400" />
          System Information
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 rounded-lg bg-black/30">
            <p className="text-gray-400 text-xs">GPU</p>
            <p className="text-white font-medium">NVIDIA RTX 4090</p>
          </div>
          <div className="p-3 rounded-lg bg-black/30">
            <p className="text-gray-400 text-xs">CUDA Version</p>
            <p className="text-white font-medium">12.3</p>
          </div>
          <div className="p-3 rounded-lg bg-black/30">
            <p className="text-gray-400 text-xs">Driver Version</p>
            <p className="text-white font-medium">545.23.08</p>
          </div>
          <div className="p-3 rounded-lg bg-black/30">
            <p className="text-gray-400 text-xs">Docker Version</p>
            <p className="text-white font-medium">24.0.7</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-8 text-center text-gray-500 text-sm">
        <p>OpenHands GPU Dashboard • DeepSeek Powered • Built with ❤️</p>
      </footer>
    </div>
  );
}

export default App;
