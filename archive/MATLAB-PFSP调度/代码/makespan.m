function Cmax = makespan(pi, P)
% MAKESPAN 计算 PFSP 的最大完工时间 makespan
%   pi - 工件排列（1×nJobs）；P - 加工时间矩阵（nJobs×nMachines）
%   递推：C(j,m) = max(C(j-1,m), C(j,m-1)) + P(pi(j),m)，首行/首列按顺序累加

    nJobs = length(pi);
    nMachines = size(P, 2);
    C = zeros(nJobs, nMachines);

    for m = 1:nMachines
        for j = 1:nJobs
            job = pi(j);
            pt = P(job, m);
            if m == 1 && j == 1
                C(j, m) = pt;
            elseif m == 1
                C(j, m) = C(j-1, m) + pt;
            elseif j == 1
                C(j, m) = C(j, m-1) + pt;
            else
                C(j, m) = max(C(j-1, m), C(j, m-1)) + pt;
            end
        end
    end

    Cmax = C(nJobs, nMachines);
end
