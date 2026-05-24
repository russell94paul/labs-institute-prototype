import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type { UserReportResponse } from '@/types/api';

const STALE = 10 * 60 * 1000;

export const useWeeklyReport = (year: number, week: number) =>
  useQuery({
    queryKey: ['reports', 'weekly', year, week],
    queryFn: () =>
      api.get(`api/reports/weekly?year=${year}&week=${week}`).json<UserReportResponse>(),
    staleTime: STALE,
  });

export const useMonthlyReport = (year: number, month: number) =>
  useQuery({
    queryKey: ['reports', 'monthly', year, month],
    queryFn: () =>
      api.get(`api/reports/monthly?year=${year}&month=${month}`).json<UserReportResponse>(),
    staleTime: STALE,
  });

export const useReportHistory = (periodType?: 'weekly' | 'monthly', limit = 24) => {
  const params = new URLSearchParams({ limit: String(limit) });
  if (periodType) params.set('period_type', periodType);
  return useQuery({
    queryKey: ['reports', 'history', periodType, limit],
    queryFn: () =>
      api
        .get(`api/reports/history?${params.toString()}`)
        .json<{ items: UserReportResponse[]; total: number }>(),
    staleTime: STALE,
  });
};

export const useRefreshThisWeek = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => api.post('api/reports/this-week').json<UserReportResponse>(),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: ['reports'] });
    },
  });
};

export const useRefreshThisMonth = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => api.post('api/reports/this-month').json<UserReportResponse>(),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: ['reports'] });
    },
  });
};

export function useCurrentWeekReport() {
  const today = new Date();
  const year = today.getFullYear();
  const startOfYear = new Date(today.getFullYear(), 0, 4);
  const week = Math.ceil(
    ((today.getTime() - startOfYear.getTime()) / 86400000 + startOfYear.getDay() + 1) / 7
  );
  return useWeeklyReport(year, week);
}

export function useCurrentMonthReport() {
  const today = new Date();
  return useMonthlyReport(today.getFullYear(), today.getMonth() + 1);
}
