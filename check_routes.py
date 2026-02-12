from app import create_app

app = create_app()

print("Routes containing 'analysis' or 'dashboard':")
for rule in app.url_map.iter_rules():
    rule_str = str(rule.rule)
    if 'analysis' in rule_str or 'dashboard' in rule_str:
        methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"  {rule_str} -> {rule.endpoint} [{methods}]")
