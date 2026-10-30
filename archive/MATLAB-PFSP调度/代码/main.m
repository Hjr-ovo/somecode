clear; clc; close all;

%% 实验参数
% nJobsList / nMachinesList / seedList 逐项对应一组算例；seed=0 表示不固定种子
nJobsList     = [10 20];
nMachinesList = [ 4 10];
seedList      = [42 303];
Nruns         = 50;           % 每种算法在每个算例上的独立运行次数

% 四种算法采用相同的评估预算，保证对比公平
pGA.popSize = 50;   pGA.maxGen  = 200;  pGA.pc = 0.85; pGA.pm = 0.15; pGA.tournamentK = 3;
pSA.T0 = 100;       pSA.alpha   = 0.95; pSA.Lk = 50;    pSA.maxIter   = 200;
pACO.nAnts = 20;    pACO.maxIter = 500; pACO.alpha = 1; pACO.beta = 2; pACO.rho = 0.1; pACO.Q = 1;
pPSO.nParticles = 50; pPSO.maxIter = 200; pPSO.wStart = 0.9; pPSO.wEnd = 0.4; pPSO.c1 = 2; pPSO.c2 = 2;

%% 环境检查
if ~exist('makespan.m', 'file')
    error('未找到 makespan.m，请把当前文件夹切到 代码/ 目录');
end
if ~exist('算例', 'dir'), mkdir('算例'); end
fprintf('环境检查通过：基础 MATLAB + makespan.m 就绪。\n');

nCase = numel(nJobsList);
if numel(nMachinesList) ~= nCase || numel(seedList) ~= nCase
    error('nJobsList / nMachinesList / seedList 三个向量长度必须相同。');
end

%% 结果汇总
summary = struct();

%% 主循环：逐个算例求解
for ci = 1:nCase
    nJobs_     = nJobsList(ci);
    nMachines_ = nMachinesList(ci);
    seed_      = seedList(ci);

    fprintf('\n\n##################################################\n');
    fprintf('### 算例 %d/%d : %d 工件 x %d 机器 (seed=%d)\n', ci, nCase, nJobs_, nMachines_, seed_);
    fprintf('##################################################\n');

    %% 1. 生成或载入算例
    fileName = sprintf('算例/PFSP_%dx%d_seed%d.mat', nJobs_, nMachines_, seed_);
    if seed_ ~= 0 && exist(fileName, 'file')
        load(fileName);                        % 已存在则直接读，保证与历史实验一致
        fprintf('已载入已有算例：%s\n', fileName);
    else
        if seed_ ~= 0, rng(seed_); end          % 固定种子可复现
        ProcessingTime = randi([1, 9], nJobs_, nMachines_);
        nJobs = nJobs_; nMachines = nMachines_; seed = seed_;
        save(fileName, 'ProcessingTime', 'seed', 'nJobs', 'nMachines');
        fprintf('已生成并存档算例：%s\n', fileName);
    end
    P = ProcessingTime;
    fprintf('%d 工件 x %d 机器，加工时间范围 [%d, %d]\n', nJobs, nMachines, min(P(:)), max(P(:)));

    cms = zeros(Nruns, 1);

    %% 2. GA 遗传算法
    fprintf('\n----- GA 遗传算法 -----\n');
    bestGA = inf; bestPiGA = []; bestHistGA = []; times = zeros(Nruns, 1);
    for r = 1:Nruns
        rng(1000 + r);
        t0 = tic;
        [pi, cm, hist] = ga_pfsp(P, pGA);
        times(r) = toc(t0); cms(r) = cm;
        if cm < bestGA, bestGA = cm; bestPiGA = pi; bestHistGA = hist; end
    end
    meanGA = mean(cms); stdGA = std(cms); timeGA = mean(times);
    fprintf('GA %d次: best=%d mean=%.2f std=%.2f avgTime=%.3fs\n', Nruns, bestGA, meanGA, stdGA, timeGA);

    %% 3. SA 模拟退火
    fprintf('\n----- SA 模拟退火 -----\n');
    bestSA = inf; bestPiSA = []; bestHistSA = []; times = zeros(Nruns, 1);
    for r = 1:Nruns
        rng(1000 + r);
        t0 = tic;
        [pi, cm, hist] = sa_pfsp(P, pSA);
        times(r) = toc(t0); cms(r) = cm;
        if cm < bestSA, bestSA = cm; bestPiSA = pi; bestHistSA = hist; end
    end
    meanSA = mean(cms); stdSA = std(cms); timeSA = mean(times);
    fprintf('SA %d次: best=%d mean=%.2f std=%.2f avgTime=%.3fs\n', Nruns, bestSA, meanSA, stdSA, timeSA);

    %% 4. ACO 蚁群算法
    fprintf('\n----- ACO 蚁群算法 -----\n');
    bestACO = inf; bestPiACO = []; bestHistACO = []; times = zeros(Nruns, 1);
    for r = 1:Nruns
        rng(1000 + r);
        t0 = tic;
        [pi, cm, hist] = aco_pfsp(P, pACO);
        times(r) = toc(t0); cms(r) = cm;
        if cm < bestACO, bestACO = cm; bestPiACO = pi; bestHistACO = hist; end
    end
    meanACO = mean(cms); stdACO = std(cms); timeACO = mean(times);
    fprintf('ACO %d次: best=%d mean=%.2f std=%.2f avgTime=%.3fs\n', Nruns, bestACO, meanACO, stdACO, timeACO);

    %% 5. PSO 粒子群
    fprintf('\n----- PSO 粒子群 -----\n');
    bestPSO = inf; bestPiPSO = []; bestHistPSO = []; times = zeros(Nruns, 1);
    for r = 1:Nruns
        rng(1000 + r);
        t0 = tic;
        [pi, cm, hist] = pso_pfsp(P, pPSO);
        times(r) = toc(t0); cms(r) = cm;
        if cm < bestPSO, bestPSO = cm; bestPiPSO = pi; bestHistPSO = hist; end
    end
    meanPSO = mean(cms); stdPSO = std(cms); timePSO = mean(times);
    fprintf('PSO %d次: best=%d mean=%.2f std=%.2f avgTime=%.3fs\n', Nruns, bestPSO, meanPSO, stdPSO, timePSO);

    %% 6. 横向对比表
    fprintf('\n===== 四算法对比（%dx%d，各 %d 次）=====\n', nJobs, nMachines, Nruns);
    fprintf('%-8s %8s %8s %8s %10s   最优排列\n', '算法', 'best', 'mean', 'std', 'avgTime(s)');
    fprintf('%-8s %8d %8.2f %8.2f %10.3f   %s\n', 'GA',  bestGA,  meanGA,  stdGA,  timeGA,  num2str(bestPiGA));
    fprintf('%-8s %8d %8.2f %8.2f %10.3f   %s\n', 'SA',  bestSA,  meanSA,  stdSA,  timeSA,  num2str(bestPiSA));
    fprintf('%-8s %8d %8.2f %8.2f %10.3f   %s\n', 'ACO', bestACO, meanACO, stdACO, timeACO, num2str(bestPiACO));
    fprintf('%-8s %8d %8.2f %8.2f %10.3f   %s\n', 'PSO', bestPSO, meanPSO, stdPSO, timePSO, num2str(bestPiPSO));

    % 随机排列基线：2000 次随机排列的平均 makespan，作为"什么都不做"的对照
    Nref = 2000;
    refCms = zeros(Nref, 1);
    rng(2024);
    for k = 1:Nref
        refCms(k) = makespan(randperm(nJobs), P);
    end
    refC = mean(refCms);
    fprintf('\n随机排列参考基线：%d 次随机排列平均 makespan = %.2f（四智能算法均应明显优于之）\n', Nref, refC);

    % 交叉校验：用独立实现 makespan_ref 核对评价结果一致
    fprintf('\n[交叉校验] makespan 与 makespan_ref 一致性：\n');
    fprintf('  GA : %d vs %d  equal=%d\n',  makespan(bestPiGA, P),  makespan_ref(bestPiGA, P),  makespan(bestPiGA, P) == makespan_ref(bestPiGA, P));
    fprintf('  SA : %d vs %d  equal=%d\n',  makespan(bestPiSA, P),  makespan_ref(bestPiSA, P),  makespan(bestPiSA, P) == makespan_ref(bestPiSA, P));
    fprintf('  ACO: %d vs %d  equal=%d\n',  makespan(bestPiACO, P), makespan_ref(bestPiACO, P), makespan(bestPiACO, P) == makespan_ref(bestPiACO, P));
    fprintf('  PSO: %d vs %d  equal=%d\n',  makespan(bestPiPSO, P), makespan_ref(bestPiPSO, P), makespan(bestPiPSO, P) == makespan_ref(bestPiPSO, P));

    % 7.1 甘特图：本算例全局最优排列
    [~, idx] = min([bestGA, bestSA, bestACO, bestPSO]);
    switch idx
        case 1, bestPiAll = bestPiGA; bestAll = bestGA; bestName = 'GA';
        case 2, bestPiAll = bestPiSA; bestAll = bestSA; bestName = 'SA';
        case 3, bestPiAll = bestPiACO; bestAll = bestACO; bestName = 'ACO';
        case 4, bestPiAll = bestPiPSO; bestAll = bestPSO; bestName = 'PSO';
    end
    % 注意：gantt_pfsp 内部已新建绘图窗口，此处不要再调用 figure，
    %       否则会多出一个空白窗口（表现为"甘特图显示不出来"）
    gantt_pfsp(bestPiAll, P, sprintf('PFSP 最优调度甘特图（%dx%d, %s, makespan=%d）', nJobs, nMachines, bestName, bestAll));

    % 7.2 收敛曲线：横轴为各算法的真实迭代次数，不做归一化。
    %     四种算法迭代轮数不同（GA/SA/PSO 各 200，ACO 500），曲线终点即各自的迭代预算。
    figure('Name', sprintf('收敛曲线 %dx%d', nJobs, nMachines));
    hold on;
    plot(1:numel(bestHistGA),  bestHistGA,  'LineWidth', 1.5);
    plot(1:numel(bestHistSA),  bestHistSA,  'LineWidth', 1.5);
    plot(1:numel(bestHistACO), bestHistACO, 'LineWidth', 1.5);
    plot(1:numel(bestHistPSO), bestHistPSO, 'LineWidth', 1.5);
    hold off;
    xlabel('迭代次数'); ylabel('当前最优 makespan');
    title(sprintf('四算法收敛曲线对比（%dx%d）', nJobs, nMachines));
    legend('GA', 'SA', 'ACO', 'PSO', 'Location', 'northeast');
    grid on;

    % 7.3 柱状图：四算法最优 makespan 对比，叠加随机基线
    figure('Name', sprintf('对比柱状图 %dx%d', nJobs, nMachines));
    vals = [bestGA, bestSA, bestACO, bestPSO];
    bar(vals, 'FaceColor', [0.3 0.5 0.8]);
    set(gca, 'XTickLabel', {'GA', 'SA', 'ACO', 'PSO'}, 'TickDir', 'out');
    hold on;
    % 用 plot 画水平基线（R2018a 兼容，yline 需 R2018b+）
    plot([0.5 4.5], [refC refC], 'r--', 'LineWidth', 1.3);
    text(4.45, refC, sprintf('随机基线 %.1f', refC), 'Color', 'r', ...
         'HorizontalAlignment', 'right', 'VerticalAlignment', 'bottom', 'FontSize', 9);
    xlim([0.5 4.5]);
    hold off;
    ylabel('最优 makespan');
    title(sprintf('四算法最优 makespan 对比（%dx%d，越低越好）', nJobs, nMachines));
    grid on;

    %% 8. 保存本算例结果（按算例分文件，避免互相覆盖）
    resFile = sprintf('results_%dx%d_seed%d.mat', nJobs, nMachines, seed);
    save(resFile, 'bestPiGA', 'bestGA', 'bestPiSA', 'bestSA', ...
                   'bestPiACO', 'bestACO', 'bestPiPSO', 'bestPSO', ...
                   'bestHistGA', 'bestHistSA', 'bestHistACO', 'bestHistPSO', ...
                   'meanGA', 'meanSA', 'meanACO', 'meanPSO', ...
                   'stdGA', 'stdSA', 'stdACO', 'stdPSO', ...
                   'timeGA', 'timeSA', 'timeACO', 'timePSO', ...
                   'P', 'nJobs', 'nMachines', 'refC');
    fprintf('\n本算例结果已保存至 代码/%s\n', resFile);

    summary(ci).nJobs = nJobs;  summary(ci).nMachines = nMachines;  summary(ci).seed = seed;
    summary(ci).GA = [bestGA meanGA stdGA timeGA];
    summary(ci).SA = [bestSA meanSA stdSA timeSA];
    summary(ci).ACO = [bestACO meanACO stdACO timeACO];
    summary(ci).PSO = [bestPSO meanPSO stdPSO timePSO];
    summary(ci).refC = refC;
end

%% 9. 全算例汇总对比（跨规模）
if nCase > 1
    fprintf('\n\n################ 全算例汇总 ################\n');
    fprintf('%-12s %-8s %10s %10s %10s %10s %10s\n', '算例', '指标', 'GA', 'SA', 'ACO', 'PSO', '随机基线');
    for ci = 1:nCase
        s = summary(ci);
        tag = sprintf('%dx%d', s.nJobs, s.nMachines);
        fprintf('%-12s %-8s %10d %10d %10d %10d %10.2f\n', tag, 'best', s.GA(1), s.SA(1), s.ACO(1), s.PSO(1), s.refC);
        fprintf('%-12s %-8s %10.2f %10.2f %10.2f %10.2f %10s\n', '', 'mean', s.GA(2), s.SA(2), s.ACO(2), s.PSO(2), '');
        fprintf('%-12s %-8s %10.2f %10.2f %10.2f %10.2f %10s\n', '', 'std',  s.GA(3), s.SA(3), s.ACO(3), s.PSO(3), '');
        fprintf('%-12s %-8s %10.3f %10.3f %10.3f %10.3f %10s\n', '', 'time', s.GA(4), s.SA(4), s.ACO(4), s.PSO(4), '');
    end
    save('results_summary.mat', 'summary');
    fprintf('\n汇总结果已保存至 代码/results_summary.mat\n');
end

fprintf('\nmain.m 运行完毕。\n');

%% 局部函数
function gantt_pfsp(pi, P, titleStr)
% 绘制 PFSP 在给定排列下的甘特图
    n = length(pi);
    m = size(P, 2);
    P = double(P);                              % 防整型：坐标拼接会把 yc-0.4 与 0.8 四舍五入
    % 递推完工时间矩阵 C(j,k)：第 j 个位置的工件在第 k 台机器上的完工时刻
    C = zeros(n, m);
    for j = 1:n
        for k = 1:m
            if j == 1 && k == 1
                C(j, k) = P(pi(j), k);
            elseif j == 1
                C(j, k) = C(j, k-1) + P(pi(j), k);
            elseif k == 1
                C(j, k) = C(j-1, k) + P(pi(j), k);
            else
                C(j, k) = max(C(j-1, k), C(j, k-1)) + P(pi(j), k);
            end
        end
    end
    cmap = lines(n);
    figure('Name', titleStr);
    hold on;
    for j = 1:n
        for k = 1:m
            dur = P(pi(j), k);
            x0 = C(j, k) - dur;
            yc = m - k + 1;                          % 行中心：M1 在顶部第 m 行，Mm 在底部第 1 行
            rectangle('Position', [x0, yc-0.4, dur, 0.8], 'FaceColor', cmap(j, :));
            text(x0 + dur/2, yc, sprintf('%d', pi(j)), 'FontSize', 8, ...
                 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
        end
    end
    hold off;
    xlabel('时间'); ylabel('机器');
    set(gca, 'YTick', 1:m, 'YTickLabel', arrayfun(@(k) sprintf('M%d', k), (m:-1:1), 'UniformOutput', false));
    xlim([0 C(n, m) * 1.05]); ylim([0.5, m + 0.5]);
    title(sprintf('%s', titleStr));
end
