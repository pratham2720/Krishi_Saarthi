import { useEffect, useState } from 'react';
import { apiGet } from '@/lib/api';
export function DemoNotice() {
  const [demo, setDemo] = useState(false);
  useEffect(() => { apiGet<{demo_mode: boolean}>('/api/runtime').then(data => setDemo(data.demo_mode)).catch(() => {}); }, []);
  if (!demo) return null;
  return <div role="status" className="bg-amber-100 text-amber-950 px-4 py-2 text-center text-sm border-b border-amber-200">
    <strong>Presentation mode.</strong> Weather and satellite readings are simulated; chat uses preset guidance. Farm records are saved locally. Predictions are illustrative.
  </div>;
}
