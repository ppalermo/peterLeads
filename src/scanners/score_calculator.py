class ScoreCalculator:
    def calculate_score(self, scan_results: dict) -> dict:
        score = 0
        reasons = []
        
        # SEO Issues (-10 points each)
        if scan_results.get('seo_issues'):
            score -= len(scan_results['seo_issues']) * 10
            if len(scan_results['seo_issues']) > 3:
                reasons.append("Multiple SEO issues need attention")
        
        # Mobile Issues (-20 points)
        if not scan_results.get('mobile_friendly', True):
            score -= 20
            reasons.append("Not mobile-friendly")
        
        # Security Issues (-15 points each)
        if scan_results.get('security_issues'):
            score -= len(scan_results['security_issues']) * 15
            reasons.append("Security vulnerabilities detected")
        
        # Performance Score
        performance = scan_results.get('performance_score', 0)
        if performance < 50:
            score -= 20
            reasons.append("Poor website performance")
        
        # Outdated Technology
        if scan_results.get('outdated_tech'):
            score -= 15
            reasons.append("Using outdated technology")
        
        return {
            'score': max(0, 100 + score),  # Don't go below 0
            'flag_reason': '; '.join(reasons)
        } 