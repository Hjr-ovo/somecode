function [bestPi, bestCmax, bestHist] = ga_pfsp(P, params)
% GA_PFSP 遗传算法求解 PFSP，最小化 makespan
%   params 字段（均可缺省）：popSize / maxGen / pc / pm / tournamentK / seed
%   算子：排列编码 / 锦标赛选择 / OX 顺序交叉 / swap 变异 / 精英保留

    if nargin < 2
        params = struct();
    end

    popSize = getf(params, 'popSize', 50);
    maxGen  = getf(params, 'maxGen', 200);
    pc      = getf(params, 'pc', 0.85);
    pm      = getf(params, 'pm', 0.15);
    K       = getf(params, 'tournamentK', 3);
    if isfield(params, 'seed') && ~isempty(params.seed)
        rng(params.seed);
    end

    n = size(P, 1);

    % 初始化种群
    pop = zeros(popSize, n);
    for i = 1:popSize
        pop(i, :) = randperm(n);
    end
    fits = zeros(popSize, 1);
    for i = 1:popSize
        fits(i) = makespan(pop(i, :), P);
    end

    [bestCmax, bi] = min(fits);
    bestPi = pop(bi, :);
    bestHist = zeros(maxGen, 1);

    for gen = 1:maxGen
        % 精英保留
        [~, ei] = min(fits);
        newPop = zeros(popSize, n);
        newPop(1, :) = pop(ei, :);

        i = 2;
        while i <= popSize
            % 锦标赛选择父母
            p1 = tournament_select(pop, fits, K);
            p2 = tournament_select(pop, fits, K);
            % 交叉
            if rand < pc
                c1 = ox_cross(p1, p2);
                if i + 1 <= popSize
                    c2 = ox_cross(p2, p1);
                else
                    c2 = c1;
                end
            else
                c1 = p1; c2 = p2;
            end
            % 变异
            if rand < pm, c1 = swap_mut(c1); end
            if rand < pm, c2 = swap_mut(c2); end
            newPop(i, :) = c1;
            if i + 1 <= popSize, newPop(i + 1, :) = c2; end
            i = i + 2;
        end

        pop = newPop;
        for k = 1:popSize
            fits(k) = makespan(pop(k, :), P);
        end

        [curBest, ci] = min(fits);
        bestHist(gen) = curBest;
        if curBest < bestCmax
            bestCmax = curBest;
            bestPi = pop(ci, :);
        end
    end
end

% ---------- 子函数 ----------

function winner = tournament_select(pop, fits, K)
    popSize = size(pop, 1);
    idx = randperm(popSize, K);
    [~, b] = min(fits(idx));
    winner = pop(idx(b), :);
end

function child = ox_cross(p1, p2)
    % 顺序交叉 OX：从 p1 取一段，其余位置按 p2 顺序填充，保证合法排列
    n = length(p1);
    a = randi(n); b = randi(n);
    if a > b, t = a; a = b; b = t; end
    child = zeros(1, n);
    child(a:b) = p1(a:b);
    seg = p1(a:b);
    rest = setdiff(p2, seg);
    pos = 1;
    for i = 1:n
        if i < a || i > b
            child(i) = rest(pos);
            pos = pos + 1;
        end
    end
end

function p = swap_mut(p)
    % 交换变异：随机交换两个不同位置，保持合法排列
    n = length(p);
    i = randi(n); j = randi(n);
    while i == j
        j = randi(n);
    end
    tmp = p(i); p(i) = p(j); p(j) = tmp;
end

function v = getf(s, name, default)
% 取结构体字段，缺省时用默认值
    if isfield(s, name)
        v = s.(name);
    else
        v = default;
    end
end
