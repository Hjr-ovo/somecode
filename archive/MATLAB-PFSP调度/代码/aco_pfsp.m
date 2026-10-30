function [bestPi, bestCmax, bestHist] = aco_pfsp(P, params)
% ACO_PFSP 蚁群算法（位置模型）求解 PFSP，最小化 makespan
%   params 字段（均可缺省）：nAnts / maxIter / alpha / beta / rho / Q / seed
%   位置模型 τ(i,j)：把工件 i 放在第 j 个位置的吸引力（nJobs×nJobs）
%   构造时逐位置轮盘赌选工件，更新时先蒸发再按 Q/C 全蚂蚁沉积
%   评估预算 nAnts*maxIter = 10000，与其它算法量级一致，便于公平对比

    if nargin < 2
        params = struct();
    end

    nJobs   = size(P, 1);
    nAnts   = getf(params, 'nAnts', 20);
    maxIter = getf(params, 'maxIter', 500);
    alpha   = getf(params, 'alpha', 1);
    beta    = getf(params, 'beta', 2);
    rho     = getf(params, 'rho', 0.1);
    Q       = getf(params, 'Q', 1);
    seed    = getf(params, 'seed', 0);
    if seed > 0
        rng(seed);
    end

    % 启发式：平均工时越短的工件越优先，归一化到最大值为 1
    eta = 1 ./ mean(P, 2);
    eta = eta / max(eta);

    % 信息素初值
    tau0 = 1 / (nJobs * mean(P(:)));
    tau  = tau0 * ones(nJobs, nJobs);

    bestC   = inf;
    bestPi  = (1:nJobs);
    bestHist = zeros(maxIter, 1);

    for it = 1:maxIter
        % 所有蚂蚁本代构造解
        ants  = zeros(nAnts, nJobs);
        costs = zeros(nAnts, 1);

        for k = 1:nAnts
            pi = zeros(1, nJobs);
            unvisited = (1:nJobs)';
            for j = 1:nJobs
                cand    = unvisited;
                tauCol  = tau(cand, j);
                etaCand = eta(cand);
                prob    = (tauCol .^ alpha) .* (etaCand .^ beta);
                % 轮盘赌选择
                cum = cumsum(prob);
                r   = rand * cum(end);
                idx = find(cum >= r, 1, 'first');
                chosen = cand(idx);
                pi(j)  = chosen;
                unvisited(idx) = [];         % 移除已选，保证排列合法
            end
            ants(k, :) = pi;
            costs(k)   = makespan(pi, P);
        end

        % 本代最优
        [cMin, bestK] = min(costs);
        if cMin < bestC
            bestC  = cMin;
            bestPi = ants(bestK, :);
        end
        bestHist(it) = bestC;

        % 信息素更新：先全局蒸发
        tau = (1 - rho) * tau;

        % 每只蚂蚁按 Q/C 在其经过的 (i,j) 上沉积
        for k = 1:nAnts
            pi     = ants(k, :);
            deposit = Q / costs(k);
            for j = 1:nJobs
                i = pi(j);
                tau(i, j) = tau(i, j) + deposit;
            end
        end
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
