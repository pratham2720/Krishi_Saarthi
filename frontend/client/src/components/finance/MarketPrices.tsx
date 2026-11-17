import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { apiGet } from '@/lib/api';

type MarketData = {
  data_source: string; disclaimer: string;
  prices: { crop: string; msp: number | null; estimated_range: { low: number; high: number }; unit: string }[];
  tips: { icon: string; text: string }[];
};
const rupees = (value: number) => `₹${value.toLocaleString('en-IN')}`;

export function MarketPrices() {
  const [data, setData] = useState<MarketData | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  async function refresh() {
    setLoading(true); setError('');
    try { setData(await apiGet<MarketData>('/finance/market-prices')); }
    catch (err) { setError(err instanceof Error ? err.message : 'Unable to load prices.'); }
    finally { setLoading(false); }
  }
  useEffect(() => { refresh(); }, []);
  const prices = data?.prices.filter(p => p.crop.toLowerCase().includes(search.toLowerCase())) || [];
  return <div className="space-y-6 pb-10">
    <div className="flex justify-between items-center gap-4"><div>
      <h1 className="text-2xl font-bold">Market Prices</h1>
      <p className="text-muted-foreground">Reference MSP and indicative price ranges</p>
    </div><Button variant="outline" onClick={refresh} disabled={loading}>Refresh</Button></div>
    <div className="rounded-lg border bg-amber-50 text-amber-950 p-4 text-sm">
      {data?.disclaimer || 'These are reference prices, not a live mandi feed.'}
      {data && <p className="font-medium mt-2">Source: {data.data_source}</p>}
    </div>
    <Input aria-label="Search commodities" placeholder="Search commodities…" value={search} onChange={e => setSearch(e.target.value)} className="max-w-md" />
    {error && <p role="alert" className="text-destructive">{error}</p>}
    {loading ? <p>Loading reference prices…</p> : <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
      {prices.map(price => <Card key={price.crop}><CardHeader><CardTitle>{price.crop}</CardTitle></CardHeader><CardContent className="space-y-3">
        <div><p className="text-sm text-muted-foreground">MSP / {price.unit}</p><p className="text-2xl font-bold">{price.msp ? rupees(price.msp) : 'Not specified'}</p></div>
        <p className="text-sm">Estimated range: <strong>{rupees(price.estimated_range.low)}–{rupees(price.estimated_range.high)}</strong></p>
      </CardContent></Card>)}
      {!prices.length && !error && <p>No matching commodities.</p>}
    </div>}
    {data?.tips.map((tip, i) => <p key={i} className="text-sm text-muted-foreground">{tip.icon} {tip.text}</p>)}
  </div>;
}
