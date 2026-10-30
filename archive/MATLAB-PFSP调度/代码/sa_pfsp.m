function [bestPi, bestCmax, bestHist] = sa_pfsp(P, params)
% SA_PFSP 模拟退火算法求解 PFSP，最小化 makespan
%   params 字段（均可缺省）：T0 / alpha / Lk / maxIter / seed
%   邻域为 swap 交换；更优必接受，更差按 exp(-delta/T) 接受；几何降温 T <- T*alpha
%   评估预算 Lk*maxIter = 10000，与其它算法量级一致，便于公平对比

    if nargin < 2
        params = struct();
    end

    nJobs   = size(P, 1);
    T0      = getf(params, 'T0', 100);
    alpha   = getf(params, 'alpha', 0.95);
    Lk      = getf(params, 'Lk', 50);
    maxIter = getf(params, 'maxIter', 200);
    seed    = getf(params, 'seed', 0);
    if seed > 0
        rng(seed);
    end

    % 初始解：随机排列
    cur    = randperm(nJobs);
    curC   = makespan(cur, P);
    bestPi = cur;
    bestC  = curC;

    T = T0;
    bestHist = zeros(maxIter, 1);

    for it = 1:maxIter
        for k = 1:Lk
            % 邻域：swap 交换两个不同位置
            i = randi(nJobs);
            j = randi(nJobs);
            while i == j
                j = randi(nJobs);
            end
            new     = cur;
            new([i j]) = new([j i]);
            newC    = makespan(new, P);
            delta   = newC - curC;

            % Metropolis 接受准则
            if delta <= 0 || rand < exp(-delta / T)
                cur  = new;
                curC = newC;
                if curC < bestC
                    bestC  = curC;
                    bestPi = cur;
                end
            end
        end
        bestHist(it) = bestC;
        T = T * alpha;   % 几何降温
    end

    bestCmax = bestC;
end

function v = getf(s, name, default)
% 取结构体字段，缺省时用默认值
    if isfield(s, name)
        v = s.(name);
    else
        v = default;
    end
end
