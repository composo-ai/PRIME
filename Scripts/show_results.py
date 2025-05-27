import json
from collections import defaultdict

def analyze_win_rates(data):
    """Analyze win rate statistics"""
    
    # Initialize counters
    counters = {
        'composo_win': 0,
        'claude_win': 0,
        'openai_win': 0,
        'total_comparisons': 0
    }
    
    # Statistics by criterion
    criterion_stats = defaultdict(lambda: {
        'composo_win': 0,
        'claude_win': 0, 
        'openai_win': 0,
        'total': 0
    })
    
    # Statistics by datasource
    datasource_stats = defaultdict(lambda: {
        'composo_win': 0,
        'claude_win': 0,
        'openai_win': 0, 
        'total': 0
    })
    
    # Iterate through data
    for item in data:
        counters['total_comparisons'] += 1
        criterion = item.get('criterion', 'unknown')
        datasource = item.get('datasource', 'unknown')
        
        # Count overall win rates
        if item.get('composo_win', False):
            counters['composo_win'] += 1
        if item.get('claude_win', False):
            counters['claude_win'] += 1
        if item.get('openai_win', False):
            counters['openai_win'] += 1
        
        # Statistics by criterion
        criterion_stats[criterion]['total'] += 1
        if item.get('composo_win', False):
            criterion_stats[criterion]['composo_win'] += 1
        if item.get('claude_win', False):
            criterion_stats[criterion]['claude_win'] += 1
        if item.get('openai_win', False):
            criterion_stats[criterion]['openai_win'] += 1
            
        # Statistics by datasource
        datasource_stats[datasource]['total'] += 1
        if item.get('composo_win', False):
            datasource_stats[datasource]['composo_win'] += 1
        if item.get('claude_win', False):
            datasource_stats[datasource]['claude_win'] += 1
        if item.get('openai_win', False):
            datasource_stats[datasource]['openai_win'] += 1
    
    return counters, criterion_stats, datasource_stats

def calculate_win_rate(wins, total):
    """Calculate win rate percentage"""
    return (wins / total * 100) if total > 0 else 0

def print_results(counters, criterion_stats, datasource_stats):
    """Print results"""
    
    total = counters['total_comparisons']
    
    print("=" * 60)
    print("Overall Win Rate Statistics")
    print("=" * 60)
    print(f"Total Comparisons: {total}")
    print(f"Composo Win Rate: {counters['composo_win']}/{total} ({calculate_win_rate(counters['composo_win'], total):.1f}%)")
    print(f"Claude Win Rate: {counters['claude_win']}/{total} ({calculate_win_rate(counters['claude_win'], total):.1f}%)")
    print(f"OpenAI Win Rate: {counters['openai_win']}/{total} ({calculate_win_rate(counters['openai_win'], total):.1f}%)")
    
    print("\n" + "=" * 60)
    print("Statistics by Criterion")
    print("=" * 60)
    for criterion, stats in criterion_stats.items():
        print(f"\n{criterion}:")
        print(f"  Total: {stats['total']}")
        print(f"  Composo: {stats['composo_win']}/{stats['total']} ({calculate_win_rate(stats['composo_win'], stats['total']):.1f}%)")
        print(f"  Claude: {stats['claude_win']}/{stats['total']} ({calculate_win_rate(stats['claude_win'], stats['total']):.1f}%)")
        print(f"  OpenAI: {stats['openai_win']}/{stats['total']} ({calculate_win_rate(stats['openai_win'], stats['total']):.1f}%)")
    
    print("\n" + "=" * 60)
    print("Statistics by Datasource")
    print("=" * 60)
    for datasource, stats in datasource_stats.items():
        print(f"\n{datasource}:")
        print(f"  Total: {stats['total']}")
        print(f"  Composo: {stats['composo_win']}/{stats['total']} ({calculate_win_rate(stats['composo_win'], stats['total']):.1f}%)")
        print(f"  Claude: {stats['claude_win']}/{stats['total']} ({calculate_win_rate(stats['claude_win'], stats['total']):.1f}%)")
        print(f"  OpenAI: {stats['openai_win']}/{stats['total']} ({calculate_win_rate(stats['openai_win'], stats['total']):.1f}%)")

def analyze_score_comparison(data):
    """Analyze score comparison"""
    print("\n" + "=" * 60)
    print("Score Statistics")
    print("=" * 60)
    
    composo_scores = []
    chosen_openai_scores = []
    rejected_openai_scores = []
    chosen_claude_scores = []
    rejected_claude_scores = []
    
    for item in data:
        if 'chosen_composo' in item:
            composo_scores.append(item['chosen_composo'])
        if 'chosen_openai' in item:
            chosen_openai_scores.append(item['chosen_openai'])
        if 'rejected_openai' in item:
            rejected_openai_scores.append(item['rejected_openai'])
        if 'chosen_claude' in item:
            chosen_claude_scores.append(item['chosen_claude'])
        if 'rejected_claude' in item:
            rejected_claude_scores.append(item['rejected_claude'])
    
    def print_score_stats(scores, name):
        if scores:
            avg = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            print(f"{name}: Average {avg:.2f}, Min {min_score:.2f}, Max {max_score:.2f}, Sample Count {len(scores)}")
    
    print_score_stats(composo_scores, "Composo Scores")
    print_score_stats(chosen_openai_scores, "OpenAI Chosen Scores")
    print_score_stats(rejected_openai_scores, "OpenAI Rejected Scores")
    print_score_stats(chosen_claude_scores, "Claude Chosen Scores")
    print_score_stats(rejected_claude_scores, "Claude Rejected Scores")

def main():
    
    with open('results/merged_evaluation.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    counters, criterion_stats, datasource_stats = analyze_win_rates(data)
    print_results(counters, criterion_stats, datasource_stats)
    analyze_score_comparison(data)

if __name__ == "__main__":
    main()