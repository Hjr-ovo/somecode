function [bestPi, bestCmax, bestHist] = pso_pfsp(P, params)
% PSO_PFSP 粒子群优化（随机键编码）求解 PFSP，最小化 makespan
%   params 字段（均可缺省）：nParticles / maxIter / wStart / wEnd / c1 / c2 / seed
%   随机键编码：粒子位置 X∈[0,1]^n，排序后的索引顺序即合法排列 π = sort(X)
%   评估预算 nParticles*maxIter = 10000，与其它算法量级一致，便于公平对比

    if nargin < 2
        params = struct();
    end

    nJobs      = size(P, 1);
    nParticles = getf(params, 'nParticles', 50);
    maxIter    = getf(params, 'maxIter', 200);
    wStart     = getf(params, 'wStart', 0.9);
    wEnd       = getf(params, 'wEnd', 0.4);
    c1         = getf(params, 'c1', 2);
    c2         = getf(params, 'c2', 2);
    seed       = getf(params, 'seed', 0);
    if seed > 0
        rng(seed);
    end

    % 初始化粒子群（随机键）
    X = rand(nParticles, nJobs);
    V = zeros(nParticles, nJobs);
    pbestX = X;
    pbestC = inf(nParticles, 1);
    gbestX = zeros(1, nJobs);
    gbestC = inf;
    bestHist = zeros(maxIter, 1);

    % 评估初始种群，记录 pbest / gbest
    for i = 1:nParticles
        [~, pi] = sort(X(i, :));
        c = makespan(pi, P);
        pbestC(i) = c;
        if c < gbestC
            gbestC = c;
            gbestX = X(i, :);
        end
    end

    for it = 1:maxIter
        % 惯性权重线性递减：前期大步探索，末期小步收敛
        if maxIter > 1
            w = wStart + (wEnd - wStart) * (it - 1) / (maxIter - 1);
        else
            w = wStart;
        end

        for i = 1:nParticles
            r1 = rand(1, nJobs);
            r2 = rand(1, nJobs);
            % 标准 PSO 速度更新
            V(i, :) = w * V(i, :) + c1 * r1 .* (pbestX(i, :) - X(i, :)) ...
                                 + c2 * r2 .* (gbestX    - X(i, :));
            % 速度钳制，防止数值爆炸
            V(i, :) = max(min(V(i, :), 1), -1);
            % 位置更新并钳到 [0,1]
            X(i, :) = X(i, :) + V(i, :);
            X(i, :) = max(min(X(i, :), 1), 0);

            % 解码（排序取索引）并评估
            [~, pi] = sort(X(i, :));
            c = makespan(pi, P);

            % 更新个体最优
            if c < pbestC(i)
                pbestC(i) = c;
                pbestX(i, :) = X(i, :);
            end
            % 更新全局最优
            if c < gbestC
                gbestC = c;
                gbestX = X(i, :);
            end
        end
        bestHist(it) = gbestC;
    end

    [~, bestPi] = sort(gbestX);
    bestCmax = gbestC;
end

function v = getf(s, name, default)
% 取结构体字段，缺省时用默认值
    if isfield(s, name)
        v = s.(name);
    else
        v = default;
    end
end
