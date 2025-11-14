import React, { useState, useEffect, useRef } from 'react';
import * as Plotly from 'plotly';

const SeminarVisualizations = () => {
  const [activeTab, setActiveTab] = useState('architecture');
  const plotRef = useRef(null);

  useEffect(() => {
    if (plotRef.current) {
      const tabData = getTabData(activeTab);
      Plotly.newPlot(plotRef.current, tabData.data, tabData.layout, {
        displayModeBar: true,
        displaylogo: false,
        toImageButtonOptions: {
          format: 'png',
          filename: `single-cell-${activeTab}`,
          height: 1080,
          width: 1920,
          scale: 2
        }
      });
    }
  }, [activeTab]);

  const getTabData = (tabId) => {
    const commonLayout = {
      paper_bgcolor: '#1e293b',
      plot_bgcolor: '#0f172a',
      font: { color: '#ffffff', size: 12 },
      autosize: true,
      margin: { l: 60, r: 60, t: 80, b: 60 }
    };

    switch(tabId) {
      case 'architecture':
        return {
          data: [{
            type: "sankey",
            orientation: "h",
            node: {
              pad: 15,
              thickness: 20,
              line: { color: "white", width: 0.5 },
              label: ["Users", "Streamlit UI", "Spark Master", "Spark Worker 1", "Spark Worker 2", 
                      "NiFi Orchestration", "Parquet Storage", "UMAP Viz", "QC Metrics"],
              color: ["#3b82f6", "#8b5cf6", "#f59e0b", "#fbbf24", "#fbbf24", 
                      "#10b981", "#ec4899", "#8b5cf6", "#8b5cf6"]
            },
            link: {
              source: [0, 1, 1, 2, 2, 5, 6, 6, 1, 1],
              target: [1, 2, 5, 3, 4, 6, 7, 8, 7, 8],
              value: [10, 8, 2, 4, 4, 5, 3, 2, 5, 3],
              color: ["rgba(59, 130, 246, 0.3)", "rgba(139, 92, 246, 0.3)", 
                      "rgba(245, 158, 11, 0.3)", "rgba(251, 191, 36, 0.3)",
                      "rgba(251, 191, 36, 0.3)", "rgba(16, 185, 129, 0.3)",
                      "rgba(236, 72, 153, 0.3)", "rgba(236, 72, 153, 0.3)",
                      "rgba(139, 92, 246, 0.3)", "rgba(139, 92, 246, 0.3)"]
            }
          }],
          layout: {
            ...commonLayout,
            title: {
              text: "System Architecture - Data Flow",
              font: { size: 24, color: '#ffffff' }
            },
            height: 600
          }
        };

      case 'performance':
        return {
          data: [
            {
              x: ['5K cells', '10K cells', '20K cells', '50K cells', '100K cells'],
              y: [3, 7, 18, 45, 90],
              name: 'Single Machine',
              type: 'bar',
              marker: { color: '#ef4444' }
            },
            {
              x: ['5K cells', '10K cells', '20K cells', '50K cells', '100K cells'],
              y: [2.5, 4, 7, 10, 20],
              name: 'Our Distributed Platform',
              type: 'bar',
              marker: { color: '#10b981' }
            }
          ],
          layout: {
            ...commonLayout,
            title: {
              text: "Processing Time Comparison (minutes)",
              font: { size: 24, color: '#ffffff' }
            },
            xaxis: { title: 'Dataset Size', color: '#ffffff' },
            yaxis: { title: 'Processing Time (minutes)', color: '#ffffff' },
            barmode: 'group',
            height: 600
          }
        };

      case 'cells':
        return {
          data: [{
            values: [800, 750, 700, 600, 650, 500, 550, 450],
            labels: ['CD4+ T-cell', 'CD8+ T-cell', 'B-cell', 'NK-cell', 
                     'Monocyte', 'Dendritic', 'Stem Cell', 'Macrophage'],
            type: 'pie',
            marker: {
              colors: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', 
                       '#10b981', '#14b8a6', '#06b6d4', '#6366f1']
            },
            textinfo: 'label+percent',
            textfont: { size: 14, color: '#ffffff' },
            hole: 0.4
          }],
          layout: {
            ...commonLayout,
            title: {
              text: "Cell Type Distribution (5,000 cells)",
              font: { size: 24, color: '#ffffff' }
            },
            height: 600,
            showlegend: true
          }
        };

      case 'resources':
        return {
          data: [
            {
              x: ['CPU (cores)', 'Memory (GB)', 'Storage (GB)'],
              y: [1, 1, 1],
              name: 'Spark Master',
              type: 'bar',
              marker: { color: '#f59e0b' }
            },
            {
              x: ['CPU (cores)', 'Memory (GB)', 'Storage (GB)'],
              y: [2, 2, 2],
              name: 'Spark Worker',
              type: 'bar',
              marker: { color: '#fbbf24' }
            },
            {
              x: ['CPU (cores)', 'Memory (GB)', 'Storage (GB)'],
              y: [1, 1, 0.5],
              name: 'Web App',
              type: 'bar',
              marker: { color: '#8b5cf6' }
            },
            {
              x: ['CPU (cores)', 'Memory (GB)', 'Storage (GB)'],
              y: [1, 1, 1],
              name: 'NiFi',
              type: 'bar',
              marker: { color: '#10b981' }
            }
          ],
          layout: {
            ...commonLayout,
            title: {
              text: "Resource Utilization by Component",
              font: { size: 24, color: '#ffffff' }
            },
            xaxis: { title: 'Resource Type', color: '#ffffff' },
            yaxis: { title: 'Amount', color: '#ffffff' },
            barmode: 'stack',
            height: 600
          }
        };

      case 'scalability':
        return {
          data: [
            {
              x: [5, 10, 20, 50, 100],
              y: [2.5, 4, 7, 10, 20],
              name: 'Actual Performance',
              mode: 'lines+markers',
              line: { color: '#10b981', width: 3 },
              marker: { size: 10 }
            },
            {
              x: [5, 10, 20, 50, 100],
              y: [2.5, 5, 10, 25, 50],
              name: 'Linear Scaling',
              mode: 'lines+markers',
              line: { color: '#3b82f6', width: 2, dash: 'dash' },
              marker: { size: 8 }
            },
            {
              x: [5, 10, 20, 50, 100],
              y: [3, 7, 18, 45, 90],
              name: 'Single Machine',
              mode: 'lines+markers',
              line: { color: '#ef4444', width: 2, dash: 'dot' },
              marker: { size: 8 }
            }
          ],
          layout: {
            ...commonLayout,
            title: {
              text: "Scalability Analysis: Processing Time vs Dataset Size",
              font: { size: 24, color: '#ffffff' }
            },
            xaxis: { title: 'Number of Cells (thousands)', color: '#ffffff' },
            yaxis: { title: 'Processing Time (minutes)', color: '#ffffff' },
            height: 600
          }
        };

      case 'usecases':
        return {
          data: [{
            type: "sunburst",
            labels: ["Platform", "Research", "Clinical", "Education",
                     "Cancer Biology", "Immunology", "Development",
                     "Diagnostics", "Drug Discovery",
                     "Teaching", "Projects",
                     "Tumor", "Treatment", "T-cell", "Profiling",
                     "Differentiation", "Lineage", "Markers", "Stratification",
                     "Target ID", "Screening", "Training", "Workshops", "Thesis", "Courses"],
            parents: ["", "Platform", "Platform", "Platform",
                      "Research", "Research", "Research",
                      "Clinical", "Clinical",
                      "Education", "Education",
                      "Cancer Biology", "Cancer Biology", "Immunology", "Immunology",
                      "Development", "Development", "Diagnostics", "Diagnostics",
                      "Drug Discovery", "Drug Discovery", "Teaching", "Teaching", "Projects", "Projects"],
            values: [100, 40, 35, 25,
                     15, 15, 10,
                     20, 15,
                     15, 10,
                     8, 7, 8, 7,
                     5, 5, 10, 10,
                     8, 7, 8, 7, 5, 5],
            marker: {
              colors: ['#1e293b', '#3b82f6', '#10b981', '#8b5cf6',
                       '#60a5fa', '#60a5fa', '#60a5fa',
                       '#34d399', '#34d399',
                       '#a78bfa', '#a78bfa',
                       '#93c5fd', '#93c5fd', '#93c5fd', '#93c5fd',
                       '#93c5fd', '#93c5fd', '#6ee7b7', '#6ee7b7',
                       '#6ee7b7', '#6ee7b7', '#c4b5fd', '#c4b5fd', '#c4b5fd', '#c4b5fd']
            },
            branchvalues: "total"
          }],
          layout: {
            ...commonLayout,
            title: {
              text: "Platform Use Cases & Applications",
              font: { size: 24, color: '#ffffff' }
            },
            height: 600
          }
        };

      case 'quality':
        return {
          data: [{
            x: [2847, 3200, 2100, 4500, 1800, 3800, 2600, 5200],
            y: [4.2, 3.8, 5.5, 3.2, 6.8, 3.5, 4.5, 2.9],
            mode: 'markers',
            type: 'scatter',
            name: 'Cell Quality',
            marker: {
              size: 15,
              color: [800, 750, 700, 600, 650, 500, 550, 450],
              colorscale: 'Viridis',
              showscale: true,
              colorbar: {
                title: 'Cell Count',
                titlefont: { color: '#ffffff' },
                tickfont: { color: '#ffffff' }
              }
            },
            text: ['CD4+ T-cell', 'CD8+ T-cell', 'B-cell', 'NK-cell', 
                   'Monocyte', 'Dendritic', 'Stem Cell', 'Macrophage']
          }],
          layout: {
            ...commonLayout,
            title: {
              text: "Quality Control: Gene Count vs Mitochondrial %",
              font: { size: 24, color: '#ffffff' }
            },
            xaxis: { title: 'Average Genes Detected', color: '#ffffff' },
            yaxis: { title: 'Mitochondrial % (avg)', color: '#ffffff' },
            height: 600
          }
        };

      default:
        return { data: [], layout: commonLayout };
    }
  };

  const tabs = [
    { id: 'architecture', label: '🏗️ Architecture' },
    { id: 'performance', label: '⚡ Performance' },
    { id: 'cells', label: '🧬 Cell Types' },
    { id: 'resources', label: '💻 Resources' },
    { id: 'scalability', label: '📈 Scalability' },
    { id: 'usecases', label: '🎯 Use Cases' },
    { id: 'quality', label: '✅ Quality Metrics' }
  ];

  return (
    <div className="w-full min-h-screen bg-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-2 text-center">
          📊 Scalable Single-Cell RNA-Seq Platform
        </h1>
        <h2 className="text-xl text-gray-300 mb-6 text-center">
          Interactive Seminar Visualizations
        </h2>
        
        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 mb-6 justify-center">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Visualization Container */}
        <div className="bg-slate-800 rounded-xl shadow-2xl p-6">
          <div ref={plotRef} style={{ width: '100%', height: '600px' }}></div>
        </div>

        {/* Info Panel */}
        <div className="mt-6 bg-slate-800 rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-3xl font-bold text-blue-400">5,000</div>
              <div className="text-gray-400 text-sm">Total Cells</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-400">8</div>
              <div className="text-gray-400 text-sm">Cell Types</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-400">75%</div>
              <div className="text-gray-400 text-sm">Speed Improvement</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-yellow-400">4</div>
              <div className="text-gray-400 text-sm">Services Running</div>
            </div>
          </div>
        </div>

        {/* Export Instructions */}
        <div className="mt-4 bg-slate-800 rounded-lg p-4 text-gray-300 text-sm">
          <p className="font-semibold mb-2">💡 Export Tips:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>Click the camera icon 📷 in the plot toolbar to download high-resolution PNG (1920x1080)</li>
            <li>Use these visualizations directly in your PowerPoint/PDF presentations</li>
            <li>All charts are interactive - hover for details, zoom, and pan</li>
            <li>Switch tabs to view different aspects of the platform</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default SeminarVisualizations;
