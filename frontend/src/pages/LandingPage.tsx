import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-bg-primary via-[#1A1A1D] to-[#0F0F11] text-text-primary overflow-x-hidden relative">
      {/* Animated background grid */}
      <div className="fixed inset-0 opacity-20 pointer-events-none">
        <div className="absolute inset-0" style={{
          backgroundImage: 'linear-gradient(rgba(139, 92, 246, 0.15) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(139, 92, 246, 0.15) 1.5px, transparent 1.5px)',
          backgroundSize: '50px 50px',
        }} />
      </div>

      {/* Glowing diagonal lines background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        {/* Diagonal lines with glow */}
        {[...Array(12)].map((_, i) => (
          <div
            key={i}
            className="absolute h-[200vh] w-1 opacity-30"
            style={{
              left: `${i * 10}%`,
              top: '-50%',
              transform: 'rotate(25deg)',
              background: `linear-gradient(180deg, 
                transparent 0%, 
                rgba(139, 92, 246, ${0.3 + (i % 3) * 0.2}) 30%,
                rgba(139, 92, 246, ${0.5 + (i % 3) * 0.2}) 50%,
                rgba(139, 92, 246, ${0.3 + (i % 3) * 0.2}) 70%,
                transparent 100%
              )`,
              boxShadow: `0 0 20px rgba(139, 92, 246, ${0.4 + (i % 3) * 0.2}), 
                          0 0 40px rgba(139, 92, 246, ${0.2 + (i % 3) * 0.1})`,
              animation: `pulse ${8 + (i % 3) * 2}s ease-in-out infinite`,
              animationDelay: `${i * 0.5}s`,
            }}
          />
        ))}
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 0.3;
          }
          50% {
            opacity: 0.6;
          }
        }
      `}</style>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-6 py-20">
        <div className="max-w-6xl mx-auto text-center">
          {/* Logo/Title with glow effect */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mb-8"
          >
            <h1 className="text-8xl font-bold mb-4 bg-gradient-to-r from-accent-purple via-status-active to-accent-purple bg-clip-text text-transparent"
                style={{ textShadow: '0 0 80px rgba(139, 92, 246, 0.5)' }}>
              WEAVE
            </h1>
            <p className="text-2xl text-text-secondary font-light tracking-wide">
              AI-Powered Video Orchestration
            </p>
          </motion.div>

          {/* Main description */}
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl text-text-secondary max-w-3xl mx-auto mb-12 leading-relaxed"
          >
            Turn simple ideas into coherent, long-form video content with AI-driven orchestration.
            Watch as intelligent agents weave together characters, scenes, and storylines in real-time.
          </motion.p>

          {/* CTA Button */}
          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            whileHover={{ scale: 1.05, boxShadow: '0 0 40px rgba(139, 92, 246, 0.6)' }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/studio')}
            className="px-12 py-5 bg-gradient-to-r from-accent-purple to-status-active text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-accent-purple/50 transition-all duration-300"
            style={{ boxShadow: '0 0 30px rgba(139, 92, 246, 0.4)' }}
          >
            Try It Now →
          </motion.button>

          {/* Scroll indicator */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1, y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity, delay: 1 }}
            className="mt-20 text-text-tertiary"
          >
            <div className="text-sm mb-2">Discover More</div>
            <div className="w-6 h-10 border-2 border-text-tertiary rounded-full mx-auto relative">
              <div className="w-1.5 h-2 bg-accent-purple rounded-full absolute left-1/2 -translate-x-1/2 top-2" />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Technology Showcase Section */}
      <section className="relative py-32 px-6">
        {/* Animated background elements */}
        <div className="absolute inset-0 flex items-center justify-center opacity-30 pointer-events-none overflow-hidden">
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              rotate: [0, 180, 360],
            }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            className="w-96 h-96 border border-accent-purple/30 rounded-full"
          />
          <motion.div
            animate={{
              scale: [1, 0.8, 1],
              rotate: [360, 180, 0],
            }}
            transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
            className="absolute w-64 h-64 border border-status-active/30 rounded-full"
          />
        </div>

        <div className="max-w-6xl mx-auto relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <motion.h2
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-6xl font-bold mb-6 bg-gradient-to-r from-text-primary via-accent-purple to-text-primary bg-clip-text text-transparent"
            >
              Videography & Cinema
              <br />
              <span className="text-5xl">Now Only a Keystroke Away</span>
            </motion.h2>
            <motion.p
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="text-xl text-text-secondary max-w-3xl mx-auto leading-relaxed"
            >
              Powered by cutting-edge agentic AI architecture, Weave transforms simple text into
              production-ready video content—complete with character depth, scene choreography,
              and narrative continuity.
            </motion.p>
          </motion.div>

          {/* Animated node network visualization */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="relative h-80 mb-16"
          >
            <div className="absolute inset-0 flex items-center justify-center">
              {/* Central hub */}
              <motion.div
                animate={{
                  boxShadow: [
                    '0 0 20px rgba(139, 92, 246, 0.5)',
                    '0 0 40px rgba(139, 92, 246, 0.8)',
                    '0 0 20px rgba(139, 92, 246, 0.5)',
                  ],
                }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute w-24 h-24 bg-gradient-to-br from-accent-purple to-status-active rounded-2xl flex items-center justify-center text-3xl font-bold z-10"
              >
                AI
              </motion.div>

              {/* Orbiting nodes */}
              {[
                { icon: '🎭', label: 'Characters', angle: 0, color: 'from-accent-purple/20 to-accent-purple/5', delay: 0 },
                { icon: '🎬', label: 'Scenes', angle: 90, color: 'from-status-warning/20 to-status-warning/5', delay: 0.5 },
                { icon: '💬', label: 'Dialogue', angle: 180, color: 'from-status-active/20 to-status-active/5', delay: 1 },
                { icon: '🎨', label: 'Style', angle: 270, color: 'from-status-success/20 to-status-success/5', delay: 1.5 },
              ].map((node, i) => {
                const radius = 150;
                const x = Math.cos((node.angle * Math.PI) / 180) * radius;
                const y = Math.sin((node.angle * Math.PI) / 180) * radius;

                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, scale: 0 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: 0.5 + node.delay }}
                    animate={{
                      x: [x, x * 1.1, x],
                      y: [y, y * 1.1, y],
                    }}
                    style={{
                      position: 'absolute',
                      left: '50%',
                      top: '50%',
                      transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
                    }}
                    className={`w-20 h-20 bg-gradient-to-br ${node.color} border border-accent-purple/30 rounded-xl flex flex-col items-center justify-center`}
                  >
                    <div className="text-2xl mb-1">{node.icon}</div>
                    <div className="text-xs text-text-secondary font-semibold">{node.label}</div>
                  </motion.div>
                );
              })}

              {/* Connecting lines */}
              {[0, 90, 180, 270].map((angle, i) => {
                const rotation = angle;
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, scaleX: 0 }}
                    whileInView={{ opacity: 0.3, scaleX: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.8, delay: 0.8 + i * 0.1 }}
                    className="absolute w-32 h-0.5 bg-gradient-to-r from-accent-purple to-transparent"
                    style={{
                      left: '50%',
                      top: '50%',
                      transformOrigin: 'left center',
                      transform: `rotate(${rotation}deg)`,
                    }}
                  />
                );
              })}
            </div>
          </motion.div>

          {/* Technology stats */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="grid md:grid-cols-3 gap-6 mb-12"
          >
            {[
              { label: 'AI Agents', value: '3+', description: 'Specialized orchestrators' },
              { label: 'Checkpoints', value: '7+', description: 'Quality control gates' },
              { label: 'Real-time', value: '100%', description: 'Transparent generation' },
            ].map((stat, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: 0.7 + i * 0.1 }}
                className="text-center p-6 bg-bg-secondary/50 backdrop-blur-sm border border-accent-purple/20 rounded-xl"
              >
                <div className="text-4xl font-bold text-accent-purple mb-2">{stat.value}</div>
                <div className="text-lg font-semibold text-text-primary mb-1">{stat.label}</div>
                <div className="text-sm text-text-tertiary">{stat.description}</div>
              </motion.div>
            ))}
          </motion.div>

          {/* CTA Button */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.8 }}
            className="text-center pb-8"
          >
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: '0 0 40px rgba(139, 92, 246, 0.6)' }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/studio')}
              className="px-12 py-5 bg-gradient-to-r from-accent-purple to-status-active text-white text-lg font-semibold rounded-xl shadow-lg transition-all duration-300"
              style={{ boxShadow: '0 0 30px rgba(139, 92, 246, 0.4)' }}
            >
              Experience It Now →
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="relative py-32 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-5xl font-bold text-center mb-6 text-text-primary"
          >
            How Weave Works
          </motion.h2>
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center text-text-secondary text-lg mb-20 max-w-2xl mx-auto"
          >
            A transparent, agentic approach to video generation—see every step of the creative process
          </motion.p>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="bg-bg-secondary border border-accent-purple/30 rounded-2xl p-8 hover:border-accent-purple/60 transition-all duration-300"
              style={{ boxShadow: '0 4px 20px rgba(139, 92, 246, 0.1)' }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-accent-purple to-status-active rounded-xl mb-6 flex items-center justify-center text-3xl font-bold"
                   style={{ boxShadow: '0 0 20px rgba(139, 92, 246, 0.5)' }}>
                1
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-text-primary">Describe Your Vision</h3>
              <p className="text-text-secondary leading-relaxed">
                Start with a simple idea—a character, a scene, or a story concept. The Entry Agent guides you through a conversational intake to capture your vision.
              </p>
            </motion.div>

            {/* Step 2 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="bg-bg-secondary border border-status-warning/30 rounded-2xl p-8 hover:border-status-warning/60 transition-all duration-300"
              style={{ boxShadow: '0 4px 20px rgba(245, 158, 11, 0.1)' }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-status-warning to-status-error rounded-xl mb-6 flex items-center justify-center text-3xl font-bold"
                   style={{ boxShadow: '0 0 20px rgba(245, 158, 11, 0.5)' }}>
                2
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-text-primary">Watch Agents Orchestrate</h3>
              <p className="text-text-secondary leading-relaxed">
                See the generation tree unfold in real-time. Specialized agents build characters, craft scenes, and maintain continuity—transparently showing their work.
              </p>
            </motion.div>

            {/* Step 3 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="bg-bg-secondary border border-status-success/30 rounded-2xl p-8 hover:border-status-success/60 transition-all duration-300"
              style={{ boxShadow: '0 4px 20px rgba(16, 185, 129, 0.1)' }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-status-success to-status-active rounded-xl mb-6 flex items-center justify-center text-3xl font-bold"
                   style={{ boxShadow: '0 0 20px rgba(16, 185, 129, 0.5)' }}>
                3
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-text-primary">Refine & Export</h3>
              <p className="text-text-secondary leading-relaxed">
                Edit at any checkpoint, adjust character traits, or modify scenes. The system regenerates with your feedback, maintaining consistency across the entire project.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative py-32 px-6 bg-gradient-to-b from-transparent via-bg-secondary/30 to-transparent">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-5xl font-bold text-center mb-20 text-text-primary"
          >
            Powered by Agentic Intelligence
          </motion.h2>

          <div className="grid md:grid-cols-2 gap-6">
            {[
              {
                icon: '🎭',
                title: 'Character Continuity',
                description: 'Deep character profiles with psychological depth, consistent across all scenes',
                color: 'from-accent-purple/20 to-accent-purple/5',
                borderColor: 'border-accent-purple/30',
              },
              {
                icon: '🌳',
                title: 'Transparent Generation Tree',
                description: 'See every agent, every decision, every checkpoint in real-time visual flow',
                color: 'from-status-active/20 to-status-active/5',
                borderColor: 'border-status-active/30',
              },
              {
                icon: '💬',
                title: 'Interactive Chat Control',
                description: 'Steer the creation with natural language—edit on the fly without starting over',
                color: 'from-status-warning/20 to-status-warning/5',
                borderColor: 'border-status-warning/30',
              },
              {
                icon: '🎬',
                title: 'Scene Orchestration',
                description: 'Cinematography, lighting, transitions—all handled by specialized sub-agents',
                color: 'from-status-success/20 to-status-success/5',
                borderColor: 'border-status-success/30',
              },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: i % 2 === 0 ? -30 : 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className={`bg-gradient-to-br ${feature.color} border ${feature.borderColor} rounded-2xl p-8 hover:scale-[1.02] transition-all duration-300`}
              >
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-2xl font-semibold mb-3 text-text-primary">{feature.title}</h3>
                <p className="text-text-secondary leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative py-32 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="bg-gradient-to-br from-bg-secondary via-accent-purple/10 to-bg-secondary border border-accent-purple/30 rounded-3xl p-16"
            style={{ boxShadow: '0 0 60px rgba(139, 92, 246, 0.2)' }}
          >
            <h2 className="text-5xl font-bold mb-6 text-text-primary">Ready to Create?</h2>
            <p className="text-xl text-text-secondary mb-10 leading-relaxed">
              Experience the future of AI video generation.
              <br />
              Watch agents orchestrate your vision in real-time.
            </p>
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: '0 0 50px rgba(139, 92, 246, 0.7)' }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/studio')}
              className="px-16 py-6 bg-gradient-to-r from-accent-purple to-status-active text-white text-xl font-semibold rounded-xl shadow-lg transition-all duration-300"
              style={{ boxShadow: '0 0 30px rgba(139, 92, 246, 0.5)' }}
            >
              Launch Weave Studio →
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative py-12 px-6 border-t border-border-subtle">
        <div className="max-w-6xl mx-auto text-center text-text-tertiary">
          <p className="text-sm">
            Weave — AI Orchestration for Long-Form Video Creation
          </p>
          <p className="text-xs mt-2 opacity-60">
            Powered by Anthropic Claude & Advanced Agent Architecture
          </p>
        </div>
      </footer>
    </div>
  );
}
