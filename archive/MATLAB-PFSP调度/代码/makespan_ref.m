function Cmax = makespan_ref(pi, P)
% MAKESPAN_REF 参考实现，与 makespan.m 逻辑相同但循环写法不同，用于交叉验证
    nJobs = length(pi);
    m = size(P, 2);
    C = zeros(nJobs, m);
    for j = 1:nJobs
        for mm = 1:m
            pt = P(pi(j), mm);
            if j == 1 && mm == 1
                C(j, mm) = pt;
            elseif mm == 1
                C(j, mm) = C(j-1, mm) + pt;
            elseif j == 1
                C(j, mm) = C(j, mm-1) + pt;
            else
                C(j, mm) = max(C(j-1, mm), C(j, mm-1)) + pt;
            end
        end
    end
    Cmax = C(nJobs, m);
end
