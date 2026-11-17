import { QueryClient } from '@tanstack/react-query';
import { apiFetch } from './api';
export const queryClient = new QueryClient({ defaultOptions: { queries: {
  queryFn: ({ queryKey }) => apiFetch(String(queryKey[0])),
  staleTime: 60000, retry: 1, refetchOnWindowFocus: false,
} } });
